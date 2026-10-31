"""Login/logout, dashboard, reviewer queue, demo sample downloads, and the Admin pages."""
from __future__ import annotations

from decimal import Decimal, InvalidOperation

from fastapi import APIRouter, Depends, Form, HTTPException, Query, Request
from fastapi.responses import FileResponse

from .. import audit, auth, mapping as mp, storage, workflow as wf
from ..auth import DEMO_USERS, ROLE_PERMISSIONS, require, safe_next, verify_csrf
from ..domain import Account, ClientConfig, Entity, list_clients, load_client, save_client
from .common import flash, redirect, render

router = APIRouter()
CSRF = [Depends(verify_csrf)]


def demo_mode_only(request: Request) -> None:
    """The fake-user login must not exist at all (404) unless DEMO_MODE is on."""
    if not request.app.state.settings.demo_mode:
        raise HTTPException(status_code=404)


def _db(request: Request):
    return request.app.state.db


# ------------------------------------------------------------------ authentication
@router.get("/login")
def login_page(request: Request, next_url: str = Query("/", alias="next")):
    if auth.current_user(request):
        return redirect(safe_next(next_url))
    return render(request, "login.html", demo_users=DEMO_USERS, next=safe_next(next_url),
                  oidc_enabled=request.app.state.oauth is not None)


@router.post("/login/demo", dependencies=[Depends(demo_mode_only), Depends(verify_csrf)])
def demo_login(request: Request, email: str = Form(""), role: str = Form(""), next_url: str = Form("/", alias="next")):
    person = next((u for u in DEMO_USERS if u["email"] == email), None)
    if person is None or role not in ROLE_PERMISSIONS:
        flash(request, "Pick one of the demo users and a role.", "error")
        return redirect("/login")
    user = auth.login_user(request, email=person["email"], name=person["name"], roles=[role], method="demo")
    with _db(request).tx() as conn:
        audit.record(conn, actor=user, action="login", details={"method": "demo", "note": "DEMO_MODE fake identity"})
    return redirect(safe_next(next_url))


@router.get("/auth/okta/login")
async def okta_login(request: Request, next_url: str = Query("/", alias="next")):
    oauth = request.app.state.oauth
    if oauth is None:
        raise HTTPException(status_code=404)
    request.session["post_login"] = safe_next(next_url)
    redirect_uri = request.app.state.settings.okta_redirect_uri or str(request.url_for("okta_callback"))
    return await oauth.okta.authorize_redirect(request, redirect_uri)


@router.get("/auth/okta/callback", name="okta_callback")
async def okta_callback(request: Request):
    oauth, settings = request.app.state.oauth, request.app.state.settings
    if oauth is None:
        raise HTTPException(status_code=404)
    try:
        token = await oauth.okta.authorize_access_token(request)
    except Exception:
        with _db(request).tx() as conn:
            audit.record(conn, actor={"email": "anonymous", "name": "", "roles": []}, action="login_failed", details={"method": "okta"})
        flash(request, "Okta sign-in failed. Please try again.", "error")
        return redirect("/login")
    claims = token.get("userinfo") or await oauth.okta.userinfo(token=token)
    roles = auth.roles_from_groups(claims.get("groups"), settings)
    email = claims.get("email") or claims.get("preferred_username") or claims.get("sub", "")
    if not roles or not email:
        with _db(request).tx() as conn:
            audit.record(conn, actor={"email": email or "unknown", "name": claims.get("name", ""), "roles": []},
                         action="login_denied", details={"method": "okta", "reason": "no mapped Okta group"})
        flash(request, "You signed in, but none of your Okta groups grants access to this tool.", "error")
        return redirect("/login")
    target = safe_next(request.session.get("post_login"))
    user = auth.login_user(request, email=email, name=claims.get("name") or email, roles=roles, method="okta")
    with _db(request).tx() as conn:
        audit.record(conn, actor=user, action="login", details={"method": "okta"})
    return redirect(target)


@router.post("/logout", dependencies=CSRF)
def logout(request: Request):
    user = auth.current_user(request)
    if user:
        with _db(request).tx() as conn:
            audit.record(conn, actor=user, action="logout")
    auth.logout_user(request)
    return redirect("/login")


# ------------------------------------------------------------------ dashboard + review queue
@router.get("/")
def dashboard(request: Request, user: dict = Depends(require())):
    with _db(request).read() as conn:
        jobs = conn.execute(
            """SELECT j.*, c.name AS client_name FROM jobs j JOIN clients c ON c.id = j.client_id
               ORDER BY j.updated_at DESC LIMIT 30""").fetchall() if auth.has_perm(user, "job.work") else []
        waiting = conn.execute("SELECT COUNT(*) AS n FROM jobs WHERE status IN ('mapping_submitted','export_requested')").fetchone()["n"]
    return render(request, "dashboard.html", jobs=jobs, waiting=waiting, active="home")


@router.get("/review")
def review_queue(request: Request, user: dict = Depends(require("review.queue"))):
    me = user["email"].strip().lower()
    items = []
    with _db(request).read() as conn:
        rows = conn.execute(
            """SELECT j.*, c.name AS client_name FROM jobs j JOIN clients c ON c.id = j.client_id
               WHERE j.status IN ('mapping_submitted','export_requested') ORDER BY j.updated_at""").fetchall()
        for job in rows:
            if job["status"] == "mapping_submitted":
                draft = wf.draft_for(conn, job)
                actors = {draft["created_by"], draft["submitted_by"]} if draft else set()
                items.append({"job": job, "kind": "Mapping approval", "link": f"/jobs/{job['id']}/mapping",
                              "by": draft["submitted_by"] if draft else "", "own": me in {a.lower() for a in actors if a}})
            else:
                items.append({"job": job, "kind": "Export approval", "link": f"/jobs/{job['id']}/export",
                              "by": job["export_requested_by"], "own": me in {p.lower() for p in wf.export_preparers(job) if p}})
    return render(request, "review.html", items=items, active="review")


@router.get("/demo-files/{name}")
def demo_file(request: Request, name: str, user: dict = Depends(require("job.work"))):
    """Synthetic sample reports, only in DEMO_MODE and only the known file names."""
    from ..demo.generate import DEMO_DIR, SAMPLE_FILES

    if not request.app.state.settings.demo_mode or name not in {s.filename for s in SAMPLE_FILES}:
        raise HTTPException(status_code=404)
    path = DEMO_DIR / name
    if not path.is_file():
        raise HTTPException(status_code=404)
    return FileResponse(path, filename=name, headers={"Cache-Control": "no-store"})


# ------------------------------------------------------------------ admin: audit log
@router.get("/admin/audit")
def audit_page(request: Request, action: str = "", actor: str = "", job: str = "", page: int = 1,
               user: dict = Depends(require("audit.view"))):
    per_page = 100
    job_id = int(job) if job.strip().isdigit() else None
    with _db(request).read() as conn:
        entries = audit.list_entries(conn, limit=per_page + 1, offset=(max(page, 1) - 1) * per_page,
                                     action=action or None, actor=actor or None, job_id=job_id)
        chain = audit.verify_chain(conn)
        actions = audit.distinct_actions(conn)
    return render(request, "admin_audit.html", entries=entries[:per_page], has_more=len(entries) > per_page, page=max(page, 1),
                  chain=chain, actions=actions, f_action=action, f_actor=actor, f_job=job, active="audit",
                  retention_days=request.app.state.settings.retention_days)


@router.post("/admin/purge", dependencies=CSRF)
def purge(request: Request, user: dict = Depends(require("audit.view"))):
    removed = storage.purge_expired(request.app.state.settings, _db(request), actor=user)
    flash(request, f"Retention purge finished: {len(removed)} file(s) deleted.", "success")
    return redirect("/admin/audit")


# ------------------------------------------------------------------ admin: clients
@router.get("/admin/clients")
def clients_page(request: Request, user: dict = Depends(require("admin.clients"))):
    with _db(request).read() as conn:
        clients = [load_client(conn, c["id"]) for c in list_clients(conn, active_only=False)]
    return render(request, "admin_clients.html", clients=clients, active="clients")


@router.get("/admin/clients/{client_id}")
def client_edit_page(request: Request, client_id: str, user: dict = Depends(require("admin.clients"))):
    with _db(request).read() as conn:
        client = load_client(conn, client_id)
    if client is None:
        raise HTTPException(status_code=404)
    return render(request, "admin_client.html", client=client, active="clients")


@router.post("/admin/clients/new", dependencies=CSRF)
def client_create(request: Request, name: str = Form(""), client_id: str = Form(""), entity_code: str = Form("MAIN"),
                  entity_name: str = Form(""), user: dict = Depends(require("admin.clients"))):
    import re

    slug = re.sub(r"[^a-z0-9]+", "-", (client_id or name).lower()).strip("-")
    code = re.sub(r"[^A-Z0-9]+", "", entity_code.upper()) or "MAIN"
    if not name.strip() or not slug:
        flash(request, "Enter a client name.", "error")
        return redirect("/admin/clients")
    from ..demo.seed import _chart

    with _db(request).tx() as conn:
        if load_client(conn, slug):
            flash(request, f"A client with id '{slug}' already exists.", "error")
            return redirect("/admin/clients")
        cfg = ClientConfig(id=slug, name=name.strip()[:120], description="Created by an Admin.",
                           entities=[Entity(code, (entity_name or name).strip()[:120], Decimal("100"), True, "UNR")],
                           funds={"UNR": "Unrestricted - General"}, accounts=_chart("parish", interco=False, housing=False))
        save_client(conn, cfg)
        audit.record(conn, actor=user, action="client_created", client_id=slug, details={"name": cfg.name})
    flash(request, f"Client '{name}' created with a standard payroll chart of accounts (edit the chart in the source system export in production).", "success")
    return redirect(f"/admin/clients/{slug}")


@router.post("/admin/clients/{client_id}", dependencies=CSRF)
async def client_update(request: Request, client_id: str, user: dict = Depends(require("admin.clients"))):
    form = {k: v for k, v in (await request.form()).items() if isinstance(v, str)}
    with _db(request).tx() as conn:
        client = load_client(conn, client_id)
        if client is None:
            raise HTTPException(status_code=404)
        errors: list[str] = []
        entities: list[Entity] = []
        for e in client.entities:
            try:
                pct = Decimal(form.get(f"pct_{e.code}", "0").strip() or "0")
                if pct < 0 or pct > 100:
                    raise InvalidOperation
            except InvalidOperation:
                errors.append(f"{e.code}: percentage must be a number from 0 to 100")
                pct = e.alloc_pct
            fund = form.get(f"fund_{e.code}", "")
            entities.append(Entity(e.code, (form.get(f"name_{e.code}") or e.name).strip()[:120], pct,
                                   form.get("paying") == e.code, fund if fund in client.funds else ""))
        if sum(Decimal(e.alloc_pct) for e in entities) != Decimal("100"):
            errors.append("allocation percentages must add up to exactly 100")
        if entities and not any(e.is_paying for e in entities):
            errors.append("choose which entity pays the payroll")
        due_from, due_to = form.get("due_from", ""), form.get("due_to", "")
        if len(entities) > 1 and (due_from not in client.accounts or due_to not in client.accounts):
            errors.append("choose the due-from and due-to accounts")
        if errors:
            flash(request, "Not saved: " + "; ".join(errors) + ".", "error")
            return redirect(f"/admin/clients/{client_id}")
        before = {e.code: str(e.alloc_pct) for e in client.entities}
        client.name = (form.get("name") or client.name).strip()[:120]
        client.active = form.get("active") == "on"
        client.entities, client.due_from_account, client.due_to_account = entities, due_from, due_to
        save_client(conn, client, replace_chart=False)
        audit.record(conn, actor=user, action="client_updated", client_id=client_id,
                     details={"allocation_before": before, "allocation_after": {e.code: str(e.alloc_pct) for e in entities},
                              "active": client.active})
    flash(request, "Client saved.", "success")
    return redirect(f"/admin/clients/{client_id}")
