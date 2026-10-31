"""Authentication, roles and CSRF.

Two ways in:
  * OIDC against Okta via Authlib (OKTA_ISSUER / OKTA_CLIENT_ID / OKTA_CLIENT_SECRET). Roles come from the
    Okta `groups` claim (group names configurable with OKTA_GROUP_*).
  * DEMO_MODE=true: a clearly labelled form to pick a fake user and role. Disabled (404) when DEMO_MODE is off.

Authorisation is permission-based, enforced on the server for every route (never just hidden in the UI).
"""
from __future__ import annotations

import hmac
import secrets
from typing import Any, Callable, Iterable
from urllib.parse import quote

from fastapi import Depends, HTTPException, Request

from .config import Settings

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


def roles_from_groups(groups: Iterable[str] | str | None, settings: Settings) -> list[str]:
    """Map Okta group names to application roles. No matching group -> no access (deny by default)."""
    if isinstance(groups, str):
        groups = [groups]
    names = set(groups or [])
    mapping = {settings.okta_group_preparer: "preparer", settings.okta_group_reviewer: "reviewer",
               settings.okta_group_admin: "admin"}
    return sorted({role for group, role in mapping.items() if group in names})


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


# ---------------------------------------------------------------- OIDC (Okta)
def setup_oauth(settings: Settings) -> Any | None:
    """Register Okta as an OIDC provider with Authlib. Returns None when Okta isn't configured."""
    if not settings.okta_configured:
        return None
    from authlib.integrations.starlette_client import OAuth

    oauth = OAuth()
    oauth.register(
        name="okta",
        client_id=settings.okta_client_id,
        client_secret=settings.okta_client_secret,
        server_metadata_url=f"{settings.okta_issuer}/.well-known/openid-configuration",
        client_kwargs={"scope": "openid profile email groups", "code_challenge_method": "S256"},
    )
    return oauth


def login_url(next_url: str) -> str:
    return f"/login?next={quote(next_url, safe='/')}"
