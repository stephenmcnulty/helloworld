"""Sign-in, roles and CSRF.

Sign-in is currently SELF-DECLARED: a person types their name, email and role and the app records them. Nothing
verifies that identity, so it is attribution for the audit log and the "you can't approve your own work" rule,
not security. APP_ENV=production is refused for that reason (see config.py). To add real sign-in later (e.g. Okta
OIDC), add a route that authenticates the person and calls `login_user(...)` with a verified email, name and
roles - everything downstream (roles, segregation of duties, audit) already keys off that one session object.

Authorisation is permission-based and enforced on the server for every route (never just hidden in the UI).
"""
from __future__ import annotations

import hmac
import re
import secrets
import time
from typing import Any, Callable
from urllib.parse import quote

from fastapi import Depends, HTTPException, Request

ROLE_PERMISSIONS: dict[str, set[str]] = {
    "preparer": {"job.create", "job.work", "mapping.propose"},
    "reviewer": {"job.create", "job.work", "mapping.propose", "mapping.approve", "export.approve", "review.queue"},
    "admin": {"admin.clients", "audit.view"},
}
ROLE_LABELS = {"preparer": "Preparer", "reviewer": "Reviewer", "admin": "Admin"}
ROLE_BLURBS = {
    "preparer": "Runs the wizard and proposes mappings.",
    "reviewer": "Also approves mappings and exports (never their own).",
    "admin": "Manages clients and reads the audit log. Does not prepare journals.",
}

# Suggested people for the demo script. They only pre-fill the sign-in form; anyone can type anything.
DEMO_USERS = [
    {"email": "pat.preparer@demo.example", "name": "Pat Preparer", "default_role": "preparer"},
    {"email": "rhea.reviewer@demo.example", "name": "Rhea Reviewer", "default_role": "reviewer"},
    {"email": "sam.senior@demo.example", "name": "Sam Senior", "default_role": "reviewer"},
    {"email": "alex.admin@demo.example", "name": "Alex Admin", "default_role": "admin"},
]


class AuthRequired(Exception):
    def __init__(self, next_url: str = "/"):
        self.next_url = next_url


def has_perm(user: dict | None, perm: str) -> bool:
    return bool(user) and any(perm in ROLE_PERMISSIONS.get(r, set()) for r in user.get("roles", []))


EMAIL_RE = re.compile(r"^[^@\s,;<>\"'()\[\]\\]+@[^@\s,;<>\"'()\[\]\\]+\.[^@\s,;<>\"'()\[\]\\]+$")
_CONTROL_RE = re.compile(r"[\x00-\x1f\x7f]+")


def clean_identity(name: str, email: str, role: str) -> tuple[dict | None, list[str]]:
    """Validate and normalise what was typed on the sign-in form. Returns (identity, problems)."""
    clean_name = re.sub(r"\s+", " ", _CONTROL_RE.sub(" ", name or "")).strip()
    clean_email = (email or "").strip().lower()
    problems: list[str] = []
    if not clean_name:
        problems.append("Enter your name.")
    elif len(clean_name) > 80:
        problems.append("Your name can be at most 80 characters.")
    if not clean_email:
        problems.append("Enter your email address.")
    elif len(clean_email) > 254 or not EMAIL_RE.match(clean_email):
        problems.append("That doesn't look like an email address (name@example.com).")
    if role not in ROLE_PERMISSIONS:
        problems.append("Choose a role.")
    if problems:
        return None, problems
    return {"name": clean_name, "email": clean_email, "role": role}, []


def safe_next(target: str | None) -> str:
    """Only allow same-site relative redirects (blocks open-redirect via ?next=)."""
    if target and target.startswith("/") and not target.startswith("//") and "\\" not in target and "\n" not in target:
        return target
    return "/"


def current_user(request: Request) -> dict | None:
    user = request.session.get("user")
    return user if isinstance(user, dict) and user.get("email") and user.get("roles") else None


def login_user(request: Request, *, email: str, name: str, roles: list[str], method: str) -> dict:
    request.session.clear()   # fresh session on login (no session fixation)
    user = {"email": email, "name": name, "roles": roles, "method": method}
    request.session["user"] = user
    request.session["csrf"] = secrets.token_urlsafe(32)
    return user


def logout_user(request: Request) -> None:
    request.session.clear()


# ---------------------------------------------------------------- CSRF
def csrf_token(request: Request) -> str:
    token = request.session.get("csrf")
    if not token:
        token = request.session["csrf"] = secrets.token_urlsafe(32)
    return token


async def verify_csrf(request: Request) -> None:
    expected = request.session.get("csrf", "")
    form = await request.form()
    supplied = form.get("csrf_token", "")
    if not expected or not isinstance(supplied, str) or not hmac.compare_digest(expected, supplied):
        raise HTTPException(status_code=403, detail="Your session expired or the form was tampered with. Reload the page and try again.")


# ---------------------------------------------------------------- dependencies
def require(perm: str | None = None) -> Callable[[Request], dict]:
    def dependency(request: Request) -> dict:
        user = current_user(request)
        if user is None:
            raise AuthRequired(request.url.path + (f"?{request.url.query}" if request.url.query else ""))
        if perm and not has_perm(user, perm):
            raise HTTPException(status_code=403, detail="Your role doesn't allow this action.")
        return user

    return dependency


def require_user_dep(perm: str | None = None) -> Any:
    return Depends(require(perm))


def login_url(next_url: str) -> str:
    return f"/login?next={quote(next_url, safe='/')}"


# ---------------------------------------------------------------- shared access code (hosted demo)
def access_code_ok(supplied: str, expected: str) -> bool:
    """Constant-time comparison so response timing doesn't reveal how much of the code was right."""
    return bool(expected) and hmac.compare_digest((supplied or "").strip().encode(), expected.encode())


class AttemptLimiter:
    """Blocks a client address after too many wrong access codes. In memory, so it resets on restart."""

    def __init__(self, max_failures: int = 10, window_seconds: float = 300.0, clock: Callable[[], float] = time.monotonic):
        self.max_failures, self.window, self.clock = max_failures, window_seconds, clock
        self._failures: dict[str, list[float]] = {}

    def _recent(self, key: str) -> list[float]:
        cutoff = self.clock() - self.window
        recent = [t for t in self._failures.get(key, []) if t > cutoff]
        if recent:
            self._failures[key] = recent
        else:
            self._failures.pop(key, None)
        return recent

    def blocked(self, key: str) -> bool:
        return len(self._recent(key)) >= self.max_failures

    def record_failure(self, key: str) -> None:
        self._recent(key)
        self._failures.setdefault(key, []).append(self.clock())

    def reset(self, key: str) -> None:
        self._failures.pop(key, None)


def client_key(request: Request) -> str:
    return request.client.host if request.client else "unknown"
