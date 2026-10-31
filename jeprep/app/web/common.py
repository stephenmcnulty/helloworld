"""Shared web helpers: templates, flash messages, redirects and small formatting filters."""
from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

from fastapi import Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from .. import auth
from ..domain import REPORT_TYPES, ROLE_LABELS as COLUMN_ROLE_LABELS, TARGET_SYSTEMS
from ..money import fmt_money
from ..workflow import STATUS_LABELS, STEPS

TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))


def _money(value: Any) -> str:
    return "" if value is None else fmt_money(Decimal(value))


def _us_date(value: Any) -> str:
    if isinstance(value, str) and value:
        value = date.fromisoformat(value[:10])
    return value.strftime("%m/%d/%Y") if value else ""


def _timestamp(value: Any) -> str:
    if not value:
        return ""
    return datetime.fromisoformat(value).strftime("%b %d, %Y %H:%M UTC")


templates.env.filters.update(money=_money, us_date=_us_date, timestamp=_timestamp)
templates.env.globals.update(
    ROLE_LABELS=auth.ROLE_LABELS, ROLE_BLURBS=auth.ROLE_BLURBS, COLUMN_ROLE_LABELS=COLUMN_ROLE_LABELS,
    STATUS_LABELS=STATUS_LABELS, STEPS=STEPS, TARGET_SYSTEMS=TARGET_SYSTEMS, REPORT_TYPES=REPORT_TYPES,
    has_perm=auth.has_perm,
)


def flash(request: Request, message: str, kind: str = "info") -> None:
    request.session.setdefault("flashes", []).append({"kind": kind, "message": message})


def render(request: Request, name: str, *, status_code: int = 200, **context: Any):
    session_flashes = request.session.pop("flashes", [])
    base = {
        "user": auth.current_user(request),
        "settings": request.app.state.settings,
        "flashes": session_flashes,
        "csrf_token": auth.csrf_token(request),
        "path": request.url.path,
    }
    return templates.TemplateResponse(request, name, {**base, **context}, status_code=status_code)


def redirect(url: str) -> RedirectResponse:
    return RedirectResponse(url, status_code=303)


def step_indicator(job, *, viewing: int) -> list[dict]:
    """Five-step indicator: done / current / upcoming, with links to steps the job has already reached."""
    from ..workflow import current_step

    reached = current_step(job)
    pages = {2: "upload", 3: "mapping", 4: "preview", 5: "export"}
    out = []
    for n, label in enumerate(STEPS, start=1):
        state = "done" if n < reached else "current" if n == reached else "todo"
        reachable = 2 <= n <= reached and not (n == 4 and not job["mapping_id"])
        out.append({"n": n, "label": label, "state": state, "viewing": n == viewing,
                    "href": f"/jobs/{job['id']}/{pages[n]}" if reachable else None})
    return out
