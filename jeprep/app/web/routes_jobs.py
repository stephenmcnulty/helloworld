"""The five-step wizard: intake -> upload -> mapping -> preview -> export."""
from __future__ import annotations

from datetime import date

from fastapi import APIRouter, Depends, Form, Request, UploadFile
from fastapi.responses import Response

from .. import audit, mapping as mp, workflow as wf
from ..auth import require, verify_csrf, has_perm
from ..domain import ROLE_LABELS as COLUMN_ROLE_LABELS, ROLES, SIDES, TARGET_SYSTEMS, list_clients, load_client
from ..money import parse_date, ZERO
from ..parsing import ParseError, parse_report
from ..redaction import build_model_payload, pii_columns
from ..storage import UploadError, validate_upload
from ..suggest import suggest_mapping
from .common import flash, redirect, render, step_indicator

router = APIRouter()
work = Depends(require("job.work"))
CSRF = [Depends(verify_csrf)]


def _db(request: Request):
    return request.app.state.db


def _deny(request: Request, user: dict, job, action: str, reason: str) -> None:
    """Record a refused action (own transaction, because the failed one was rolled back)."""
    with _db(request).tx() as conn:
        audit.record(conn, actor=user, action=action, client_id=job["client_id"], job_id=job["id"],
                     details={"reason": reason})


def _load(request: Request, job_id: int):
    with _db(request).read() as conn:
        job = wf.get_job(conn, job_id)
        client = load_client(conn, job["client_id"])
    return job, client


# ------------------------------------------------------------------ step 1: intake
@router.get("/jobs/new")
def intake_form(request: Request, user: dict = Depends(require("job.create"))):
    with _db(request).read() as conn:
        clients = [load_client(conn, c["id"]) for c in list_clients(conn)]
    return render(request, "intake.html", clients=clients, form={}, active="new")


@router.post("/jobs/new", dependencies=CSRF)
def intake_submit(
    request: Request,
    client_id: str = Form(""), target_system: str = Form(""), report_type: str = Form("payroll_register"),
    period_start: str = Form(""), period_end: str = Form(""), allocate: str = Form("no"),
    user: dict = Depends(require("job.create")),
):
    form = dict(client_id=client_id, target_system=target_system, report_type=report_type,
                period_start=period_start, period_end=period_end, allocate=allocate)
    try:
        with _db(request).tx() as conn:
            client = load_client(conn, client_id)
            job_id = wf.create_job(conn, user, client, target=target_system, report_type=report_type,
                                   period_start=parse_date(period_start), period_end=parse_date(period_end),
                                   allocate=(allocate == "yes"))
    except wf.WorkflowError as exc:
        with _db(request).read() as conn:
            clients = [load_client(conn, c["id"]) for c in list_clients(conn)]
        flash(request, exc.message, "error")
        return render(request, "intake.html", status_code=400, clients=clients, form=form, active="new")
    return redirect(f"/jobs/{job_id}/upload")


@router.get("/jobs/{job_id}")
def job_home(request: Request, job_id: int, user: dict = work):
    job, _ = _load(request, job_id)
    return redirect(f"/jobs/{job_id}/{wf.current_page(job)}")


# ------------------------------------------------------------------ step 2: upload
@router.get("/jobs/{job_id}/upload")
def upload_form(request: Request, job_id: int, user: dict = work):
    job, client = _load(request, job_id)
    samples = []
    if request.app.state.settings.demo_mode:
        from ..demo.generate import SAMPLE_FILES
        samples = [s for s in SAMPLE_FILES if s.client_id == client.id]
    return render(request, "upload.html", job=job, client=client, samples=samples, active="jobs",
                  steps=step_indicator(job, viewing=2), max_mb=request.app.state.settings.max_upload_bytes // (1024 * 1024))


@router.post("/jobs/{job_id}/upload", dependencies=CSRF)
async def upload_submit(request: Request, job_id: int, file: UploadFile, user: dict = work):
    settings, db = request.app.state.settings, _db(request)
    job, client = _load(request, job_id)
    # Read at most limit+1 bytes: an oversized upload is rejected without being held in memory in full.
    data = await file.read(settings.max_upload_bytes + 1)
    name = file.filename or "upload"
    try:
        ext = validate_upload(name, data, settings.max_upload_bytes)
        report = parse_report(data, ext, max_rows=settings.max_rows, max_columns=settings.max_columns)
    except (UploadError, ParseError) as exc:
        with db.tx() as conn:
            audit.record(conn, actor=user, action="file_rejected", client_id=client.id, job_id=job_id,
                         details={"reason": str(exc)[:200], "name": name[:120], "size": len(data)})
        flash(request, str(exc), "error")
        return redirect(f"/jobs/{job_id}/upload")
    try:
        with db.tx() as conn:
            job = wf.get_job(conn, job_id)
            outcome = wf.attach_upload(conn, settings, user, job, client, filename=name, ext=ext, data=data, report=report)
    except wf.WorkflowError as exc:
        flash(request, exc.message, "error")
        return redirect(f"/jobs/{job_id}/upload")
    flash(request, "Matched a saved mapping for this client's report layout." if outcome == "matched"
          else "This report layout has no approved mapping yet - review the proposed mapping below.", "success" if outcome == "matched" else "info")
    return redirect(f"/jobs/{job_id}/mapping")


# ------------------------------------------------------------------ step 3: mapping
def _column_info(report) -> dict[str, dict]:
    pii = pii_columns(report)
    info = {}
    for h in report.headers:
        values = [v for v in report.values(h) if v.strip()]
        is_amount = report.is_amount_column(h)
        info[h] = {
            "is_amount": is_amount,
            "total": report.column_total(h) if is_amount else None,
            "sample": "(redacted)" if h in pii else (values[0] if values else ""),
        }
    return info


@router.get("/jobs/{job_id}/mapping")
def mapping_page(request: Request, job_id: int, user: dict = work):
    settings = request.app.state.settings
    with _db(request).read() as conn:
        job = wf.get_job(conn, job_id)
        client = load_client(conn, job["client_id"])
        if job["status"] == "intake":
            return redirect(f"/jobs/{job_id}/upload")
        draft = wf.draft_for(conn, job)
        approved = mp.get_mapping(conn, job["mapping_id"])
    report = wf.load_report(settings, job)
    active_draft = draft is not None and draft["status"] in ("draft", "submitted", "rejected")
    if active_draft:
        mode = {"draft": "edit", "submitted": "review", "rejected": "rejected"}[draft["status"]]
        shown = draft
    else:
        mode, shown = "approved", approved
    lines = mp.lines_of(shown)
    matched = bool(approved) and mode == "approved" and approved["job_id"] != job_id
    redaction = build_model_payload(report) if mode == "edit" else None
    mapping_actors = {draft["created_by"], draft["submitted_by"]} if active_draft else set()
    me = user["email"].strip().lower()
    return render(
        request, "mapping.html", job=job, client=client, report=report, mode=mode, mapping=shown, lines=lines,
        matched=matched, col_info=_column_info(report), steps=step_indicator(job, viewing=3), active="jobs",
        role_opts=[(r, COLUMN_ROLE_LABELS[r]) for r in ROLES], side_opts=[(x, x.title()) for x in SIDES],
        account_opts=[(a.account_no, f"{a.account_no} {a.name}") for a in sorted(client.accounts.values(), key=lambda a: a.account_no)],
        entity_opts=[(e.code, e.code) for e in client.entities], fund_opts=[(c, f"{c} - {n}") for c, n in client.funds.items()],
        problems=wf.mapping_problems(lines, report, client) if mode == "edit" else [],
        redaction=redaction, ai_configured=settings.ai_configured, model=settings.anthropic_model,
        can_approve=has_perm(user, "mapping.approve"), is_author=me in {a.strip().lower() for a in mapping_actors if a},
        has_approved_fallback=bool(approved) and mode != "approved",
    )


def _form_dict(form) -> dict[str, str]:
    return {k: v for k, v in form.items() if isinstance(v, str)}


@router.post("/jobs/{job_id}/mapping/{action}", dependencies=CSRF)
async def mapping_action(request: Request, job_id: int, action: str, user: dict = work):
    """save | suggest | submit | approve | reject | reopen | change | discard | confirm"""
    settings, db = request.app.state.settings, _db(request)
    form = _form_dict(await request.form())
    back = f"/jobs/{job_id}/mapping"
    job, client = _load(request, job_id)
    approved = False
    needs_approval_perm = action in ("approve", "reject")
    if needs_approval_perm and not has_perm(user, "mapping.approve"):
        flash(request, "Only a Reviewer can approve or reject a mapping.", "error")
        return redirect(back)
    try:
        report = wf.load_report(settings, job)
        message, kind, approved = "", "success", False
        if action in ("save", "suggest", "submit"):
            with db.tx() as conn:
                job = wf.get_job(conn, job_id)
                wf.save_draft(conn, user, job, client, report, form)
                if action == "save":
                    message = "Mapping saved as a draft."
                elif action == "suggest":
                    suggestion = suggest_mapping(report, client, api_key=settings.anthropic_api_key, model=settings.anthropic_model)
                    filled = wf.apply_suggestion(conn, user, job, client, report, suggestion)
                    message = f"{suggestion.notice} {filled} unassigned column(s) were filled in - none are approved."
                    kind = "info"
                else:
                    wf.submit_mapping(conn, user, job, client, report)
                    message = "Mapping submitted. A Reviewer (not you) must approve it before a journal can be built."
        elif action in ("approve", "reject"):
            with db.tx() as conn:
                job = wf.get_job(conn, job_id)
                if action == "approve":
                    version = wf.approve_mapping(conn, user, job, client)
                    approved = True
                    message = f"Mapping approved and saved as version {version} for {client.name}."
                else:
                    wf.reject_mapping(conn, user, job, client, form.get("note", ""))
                    message, kind = "Mapping sent back to the preparer.", "info"
        elif action in ("reopen", "change", "discard"):
            with db.tx() as conn:
                job = wf.get_job(conn, job_id)
                if action == "reopen":
                    wf.reopen_mapping(conn, user, job, client)
                    message = "Mapping reopened for editing."
                elif action == "change":
                    wf.propose_changes(conn, user, job, client, report)
                    message = "A new draft was started from the approved mapping. It only replaces it once a Reviewer approves."
                else:
                    wf.discard_draft(conn, user, job, client)
                    message = "Draft discarded; the approved mapping stays in use."
        elif action == "confirm":
            return redirect(f"/jobs/{job_id}/preview")
        else:
            flash(request, "Unknown action.", "error")
            return redirect(back)
        flash(request, message, kind)
    except wf.SelfApprovalError as exc:
        _deny(request, user, job, f"mapping_{action}_denied", "segregation of duties")
        flash(request, exc.message, "error")
    except wf.WorkflowError as exc:
        flash(request, exc.message, "error")
    if action == "approve" and approved:
        return redirect(f"/jobs/{job_id}/preview")
    return redirect(back)


# ------------------------------------------------------------------ step 4: preview
@router.get("/jobs/{job_id}/preview")
def preview_page(request: Request, job_id: int, user: dict = work):
    settings = request.app.state.settings
    with _db(request).read() as conn:
        job = wf.get_job(conn, job_id)
        if not job["mapping_id"]:
            flash(request, "Approve a mapping before previewing the journal.", "info")
            return redirect(f"/jobs/{job_id}/mapping")
        preview = wf.build_preview(conn, settings, job)
    by_entity = preview.journal.by_entity()
    return render(request, "preview.html", job=job, client=preview.client, preview=preview, by_entity=by_entity,
                  steps=step_indicator(job, viewing=4), active="jobs", zero=ZERO)


@router.post("/jobs/{job_id}/request-export", dependencies=CSRF)
def request_export(request: Request, job_id: int, user: dict = work):
    try:
        with _db(request).tx() as conn:
            job = wf.get_job(conn, job_id)
            wf.request_export(conn, request.app.state.settings, user, job)
        flash(request, "Sent for approval. A Reviewer other than you must approve the export.", "success")
        return redirect(f"/jobs/{job_id}/export")
    except wf.WorkflowError as exc:
        flash(request, exc.message, "error")
        return redirect(f"/jobs/{job_id}/preview")


# ------------------------------------------------------------------ step 5: export
@router.get("/jobs/{job_id}/export")
def export_page(request: Request, job_id: int, user: dict = work):
    settings = request.app.state.settings
    with _db(request).read() as conn:
        job = wf.get_job(conn, job_id)
        if job["status"] in ("intake", "needs_mapping", "mapping_submitted", "ready"):
            return redirect(f"/jobs/{job_id}/{wf.current_page(job)}")
        preview = wf.build_preview(conn, settings, job) if job["status"] in ("export_requested", "export_approved") else None
        client = load_client(conn, job["client_id"])
    me = user["email"].strip().lower()
    preparers = {p.strip().lower() for p in wf.export_preparers(job) if p}
    return render(request, "export.html", job=job, client=client, preview=preview, steps=step_indicator(job, viewing=5),
                  active="jobs", is_preparer=me in preparers, can_approve=has_perm(user, "export.approve"),
                  retention_days=settings.retention_days, delete_default=settings.delete_after_export_default)


@router.post("/jobs/{job_id}/export/{action}", dependencies=CSRF)
async def export_action(request: Request, job_id: int, action: str, user: dict = work):
    settings, db = request.app.state.settings, _db(request)
    form = _form_dict(await request.form())
    back = f"/jobs/{job_id}/export"
    job, _ = _load(request, job_id)
    if action in ("approve", "reject") and not has_perm(user, "export.approve"):
        flash(request, "Only a Reviewer can approve or reject an export.", "error")
        return redirect(back)
    try:
        with db.tx() as conn:
            job = wf.get_job(conn, job_id)
            if action == "approve":
                wf.approve_export(conn, settings, user, job)
                flash(request, "Export approved. The import file can now be generated.", "success")
            elif action == "reject":
                wf.reject_export(conn, user, job, form.get("note", ""))
                flash(request, "Export sent back to the preparer.", "info")
                back = f"/jobs/{job_id}/preview"
            elif action == "generate":
                export = wf.generate_export(conn, settings, user, job, delete_after=form.get("delete_after") == "on")
                flash(request, f"Created {export.filename} ({export.row_count} lines). Nothing was posted to {TARGET_SYSTEMS[job['target_system']]}.", "success")
            else:
                flash(request, "Unknown action.", "error")
    except wf.SelfApprovalError as exc:
        _deny(request, user, job, f"export_{action}_denied", "segregation of duties")
        flash(request, exc.message, "error")
    except wf.WorkflowError as exc:
        flash(request, exc.message, "error")
    return redirect(back)


@router.get("/jobs/{job_id}/export/download")
def export_download(request: Request, job_id: int, user: dict = work):
    try:
        with _db(request).tx() as conn:
            job = wf.get_job(conn, job_id)
            name, data = wf.read_export(conn, request.app.state.settings, user, job)
    except wf.WorkflowError as exc:
        flash(request, exc.message, "error")
        return redirect(f"/jobs/{job_id}/export")
    return Response(data, media_type="text/csv; charset=utf-8",
                    headers={"Content-Disposition": f'attachment; filename="{name}"', "Cache-Control": "no-store"})
