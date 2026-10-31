"""Application factory. Run with:  uvicorn app.main:create_app --factory"""
from __future__ import annotations

import logging
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.sessions import SessionMiddleware

from . import auth, storage
from .config import BASE_DIR, Settings, load_dotenv
from .db import Database
from .web import routes_jobs, routes_misc
from .web.common import render
from .workflow import WorkflowError

log = logging.getLogger("jeprep")
APP_DIR = Path(__file__).resolve().parent

CSP = ("default-src 'self'; img-src 'self' data:; style-src 'self'; script-src 'self'; "
       "frame-ancestors 'none'; base-uri 'self'; form-action 'self'")


def create_app(settings: Settings | None = None) -> FastAPI:
    if settings is None:
        load_dotenv(BASE_DIR / ".env")
        settings = Settings.from_env()
    app = FastAPI(title="Journal Entry Prep (demo)", docs_url=None, redoc_url=None, openapi_url=None)
    app.state.settings = settings
    app.state.db = db = Database(settings.db_path)
    db.init_schema()
    for folder in (settings.upload_dir, settings.export_dir):
        storage.ensure_private_dir(settings.data_dir)
        storage.ensure_private_dir(folder)

    if settings.demo_mode:
        from .demo.seed import seed_demo

        if seed_demo(db):
            log.warning("DEMO_MODE: seeded synthetic clients and saved mappings.")
    log.warning("Sign-in is self-declared: names, emails and roles are not verified. Do not use with real data.")
    removed = storage.purge_expired(settings, db)
    if removed:
        log.info("Retention purge removed %d file(s) at startup.", len(removed))

    app.add_middleware(SessionMiddleware, secret_key=settings.secret_key, session_cookie="jeprep_session",
                       max_age=8 * 3600, same_site="lax", https_only=settings.cookie_secure)

    @app.middleware("http")
    async def security_headers(request: Request, call_next):
        length = request.headers.get("content-length")
        if length and length.isdigit() and int(length) > settings.max_upload_bytes + 1024 * 1024:
            return JSONResponse({"detail": "Request too large."}, status_code=413)
        response = await call_next(request)
        response.headers.setdefault("Content-Security-Policy", CSP)
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault("Referrer-Policy", "same-origin")
        if not request.url.path.startswith("/static"):
            response.headers.setdefault("Cache-Control", "no-store")
        return response

    @app.exception_handler(auth.AuthRequired)
    async def needs_login(request: Request, exc: auth.AuthRequired):
        return RedirectResponse(auth.login_url(exc.next_url), status_code=303)

    @app.exception_handler(WorkflowError)
    async def workflow_error(request: Request, exc: WorkflowError):
        return render(request, "error.html", status_code=exc.status_code, title="Can't continue", message=exc.message)

    @app.exception_handler(StarletteHTTPException)
    async def http_error(request: Request, exc: StarletteHTTPException):
        titles = {403: "Not allowed", 404: "Not found", 413: "Too large"}
        message = exc.detail if isinstance(exc.detail, str) and exc.detail not in ("Forbidden", "Not Found") else {
            403: "You don't have permission to do that.", 404: "That page doesn't exist."}.get(exc.status_code, "Something went wrong.")
        return render(request, "error.html", status_code=exc.status_code, title=titles.get(exc.status_code, "Error"), message=message)

    app.mount("/static", StaticFiles(directory=str(APP_DIR / "static")), name="static")
    app.include_router(routes_misc.router)
    app.include_router(routes_jobs.router)
    return app
