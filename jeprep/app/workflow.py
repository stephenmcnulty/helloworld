"""Job workflow: the state machine behind the five wizard steps, with segregation of duties and audit.

Statuses
  intake              job created, waiting for the source report
  needs_mapping       report uploaded, no approved mapping for this layout (a draft exists)
  mapping_submitted   draft submitted, waiting for a Reviewer (not the author) to approve
  ready               an approved mapping is attached; preview/validation available
  export_requested    preview passed all checks; waiting for a Reviewer (not the preparer) to approve
  export_approved     approved; the import file can be generated
  exported            import file generated (and, optionally, the source upload deleted)

Nothing here posts to an external system. Functions raise WorkflowError with a message that is safe to show.
"""
from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import date

from . import audit, mapping as mp
from .config import Settings
from .domain import REPORT_TYPES, TARGET_SYSTEMS, ClientConfig, MappingLine, load_client
from .exporters import ExportFile, export_journal
from .journal import DraftJournal, build_journal
from .parsing import ParsedReport, normalize_header, parse_report
from .rules import propose_from_rules
from .storage import UploadError, delete_stored, read_stored, resolve_stored, sha256_hex, store_bytes, validate_upload
from .validation import CheckResult, TieOutRow, all_passed, run_checks

STEPS = ["Intake", "Upload", "Mapping", "Preview", "Export"]
STATUS_LABELS = {
    "intake": "Waiting for upload",
    "needs_mapping": "Mapping needed",
    "mapping_submitted": "Mapping awaiting approval",
    "ready": "Ready to preview",
    "export_requested": "Export awaiting approval",
    "export_approved": "Export approved",
    "exported": "Exported",
}
_STEP_OF = {"intake": 2, "needs_mapping": 3, "mapping_submitted": 3, "ready": 4, "export_requested": 5,
            "export_approved": 5, "exported": 5}
_PAGE_OF = {2: "upload", 3: "mapping", 4: "preview", 5: "export"}


class WorkflowError(Exception):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.message, self.status_code = message, status_code


class SelfApprovalError(WorkflowError):
    def __init__(self, message: str):
        super().__init__(message, 403)


def now() -> str:
    return audit._now()


def current_step(job: sqlite3.Row) -> int:
    return _STEP_OF.get(job["status"], 2)


def current_page(job: sqlite3.Row) -> str:
    return _PAGE_OF[current_step(job)]


def get_job(conn: sqlite3.Connection, job_id: int) -> sqlite3.Row:
    job = conn.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()
    if job is None:
        raise WorkflowError("That journal entry job does not exist.", 404)
    return job


def _update(conn: sqlite3.Connection, job_id: int, **fields) -> None:
    fields["updated_at"] = now()
    cols = ", ".join(f"{k} = ?" for k in fields)
    conn.execute(f"UPDATE jobs SET {cols} WHERE id = ?", [*fields.values(), job_id])


def _different_people(user: dict, others: set[str | None], what: str) -> None:
    mine = user["email"].strip().lower()
    if mine in {o.strip().lower() for o in others if o}:
        raise SelfApprovalError(f"Blocked: you prepared this {what}, so you cannot approve it. Another Reviewer must.")


def export_preparers(job: sqlite3.Row) -> set[str | None]:
    return {job["created_by"], job["file_uploaded_by"], job["export_requested_by"]}


# ------------------------------------------------------------------ step 1: intake
def create_job(conn: sqlite3.Connection, user: dict, client: ClientConfig | None, *, target: str, report_type: str,
               period_start: date | None, period_end: date | None, allocate: bool) -> int:
    if client is None or not client.active:
        raise WorkflowError("Choose a client.")
    if target not in TARGET_SYSTEMS:
        raise WorkflowError("Choose a target system.")
    if report_type not in REPORT_TYPES:
        raise WorkflowError("Choose a report type.")
    if period_start is None or period_end is None:
        raise WorkflowError("Enter the pay period start and end dates.")
    if period_start > period_end:
        raise WorkflowError("The pay period start date is after the end date.")
    if (period_end - period_start).days > 366:
        raise WorkflowError("A pay period can't be longer than a year.")
    if allocate:
        problems = client.allocation_problems()
        if problems:
            raise WorkflowError(f"Allocation can't be used for {client.name}: " + "; ".join(problems) + ". An Admin can fix this under Clients.")
    ts = now()
    cur = conn.execute(
        """INSERT INTO jobs (client_id, target_system, report_type, period_start, period_end, allocate, status,
                             created_by, created_by_name, created_at, updated_at)
           VALUES (?, ?, ?, ?, ?, ?, 'intake', ?, ?, ?, ?)""",
        (client.id, target, report_type, period_start.isoformat(), period_end.isoformat(), int(allocate),
         user["email"], user["name"], ts, ts),
    )
    job_id = int(cur.lastrowid)
    audit.record(conn, actor=user, action="job_created", client_id=client.id, job_id=job_id,
                 details={"target": target, "report_type": report_type, "period": f"{period_start}..{period_end}", "allocate": allocate})
    return job_id


# ------------------------------------------------------------------ step 2: upload + layout detection
def load_report(settings: Settings, job: sqlite3.Row) -> ParsedReport:
    if not job["file_stored"]:
        why = "was deleted" + (f" ({job['file_delete_reason'].replace('_', ' ')})" if job["file_delete_reason"] else "")
        raise WorkflowError(f"The uploaded report {why}. Upload it again to continue.", 410)
    try:
        data = read_stored(settings.upload_dir, job["file_stored"])
    except (FileNotFoundError, UploadError):
        raise WorkflowError("The uploaded report is no longer available. Upload it again.", 410)
    return parse_report(data, job["file_ext"], max_rows=settings.max_rows, max_columns=settings.max_columns)


def propose_draft(conn: sqlite3.Connection, client: ClientConfig, report: ParsedReport, report_type: str) -> tuple[list[MappingLine], str]:
    """Rules proposal, overlaid with the client's latest approved mapping for columns that already exist there."""
    lines = propose_from_rules(report, client)
    notice = "Draft proposed by built-in rules. Nothing is approved yet."
    versions = mp.approved_versions(conn, client.id, report_type)
    if versions:
        saved = {normalize_header(l.source_column): l for l in mp.lines_of(versions[0]) if l.role}
        reused = 0
        for i, line in enumerate(lines):
            prior = saved.get(normalize_header(line.source_column))
            if prior is not None:
                lines[i] = MappingLine.from_dict({**prior.to_dict(), "source_column": line.source_column, "origin": "saved",
                                                  "reviewed": True, "rationale": f"Reused from approved mapping v{versions[0]['version']}"})
                reused += 1
        if reused:
            notice = f"Draft reuses {reused} column(s) from approved mapping v{versions[0]['version']}; the rest were proposed by built-in rules."
    return lines, notice


def attach_upload(conn: sqlite3.Connection, settings: Settings, user: dict, job: sqlite3.Row, client: ClientConfig, *,
                  filename: str, ext: str, data: bytes, report: ParsedReport) -> str:
    """Store the (already validated and parsed) upload and route to preview or mapping. Returns 'matched' or 'mapping'."""
    if job["status"] in ("export_requested", "export_approved", "exported"):
        raise WorkflowError("This journal is already in the export stage; start a new job to upload a different report.")
    from .storage import sanitize_filename

    sha = sha256_hex(data)
    if job["file_stored"]:
        delete_stored(settings.upload_dir, job["file_stored"])
        audit.record(conn, actor=user, action="file_deleted", client_id=client.id, job_id=job["id"], file_sha256=job["file_sha256"],
                     details={"reason": "replaced by a new upload"})
    stored = store_bytes(settings.upload_dir, f"job_{job['id']}", data, ext)
    match = mp.find_approved(conn, client.id, job["report_type"], report.layout_signature)
    fields = dict(file_name=sanitize_filename(filename), file_ext=ext, file_stored=stored, file_sha256=sha, file_size=len(data),
                  file_uploaded_by=user["email"], file_uploaded_at=now(), file_deleted_at=None, file_delete_reason=None,
                  layout_signature=report.layout_signature, je_hash=None)
    audit.record(conn, actor=user, action="file_uploaded", client_id=client.id, job_id=job["id"], file_sha256=sha,
                 details={"name": fields["file_name"], "size": len(data), "rows": report.row_count, "columns": len(report.headers)})
    if match is not None:
        _update(conn, job["id"], **fields, mapping_id=match["id"], draft_mapping_id=None, status="ready")
        audit.record(conn, actor=user, action="mapping_matched", client_id=client.id, job_id=job["id"],
                     mapping_version=match["version"], file_sha256=sha, details={"layout_signature": report.layout_signature[:16]})
        return "matched"
    lines, notice = propose_draft(conn, client, report, job["report_type"])
    draft_id = mp.create_draft(conn, job_id=job["id"], client_id=client.id, report_type=job["report_type"],
                               signature=report.layout_signature, headers=report.headers, lines=lines, source="rules",
                               notice=notice, user_email=user["email"])
    _update(conn, job["id"], **fields, mapping_id=None, draft_mapping_id=draft_id, status="needs_mapping")
    audit.record(conn, actor=user, action="mapping_required", client_id=client.id, job_id=job["id"], file_sha256=sha,
                 details={"layout_signature": report.layout_signature[:16], "unrecognised_columns": sum(1 for l in lines if not l.role)})
    return "mapping"


# ------------------------------------------------------------------ step 3: mapping
def draft_for(conn: sqlite3.Connection, job: sqlite3.Row) -> sqlite3.Row | None:
    return mp.get_mapping(conn, job["draft_mapping_id"])


def lines_from_form(form: dict[str, str], previous: list[MappingLine], client: ClientConfig) -> list[MappingLine]:
    """Rebuild mapping lines from the posted editor. Unknown values are kept as-is so validation can name them."""
    out: list[MappingLine] = []
    for i, prev in enumerate(previous):
        g = lambda k, i=i: (form.get(f"line_{i}_{k}") or "").strip()  # noqa: E731
        if form.get(f"line_{i}_column", prev.source_column) != prev.source_column:
            raise WorkflowError("The mapping form is out of date. Reload the page and try again.")
        role = g("role")
        line = MappingLine.from_dict({**prev.to_dict(), "role": role})
        if role == "amount":
            line.side, line.gl_account, line.offset_account = g("side"), g("gl_account"), g("offset_account")
            line.entity, line.fund = g("entity"), g("fund")
            line.line_type = client.line_type_for(line.gl_account) or line.line_type
        else:
            line.line_type = line.side = line.gl_account = line.offset_account = line.entity = line.fund = ""
        line.reviewed = form.get(f"line_{i}_reviewed") == "on"
        if line.origin not in ("ai", "mock", "rules", "saved"):
            line.origin = "manual"
        out.append(line)
    return out


def mapping_problems(lines: list[MappingLine], report: ParsedReport, client: ClientConfig) -> list[str]:
    by_col = {l.source_column: l for l in lines}
    problems: list[str] = []
    for header in report.headers:
        line = by_col.get(header)
        if line is None:
            problems.append(f"'{header}': missing from the mapping")
            continue
        problems += [f"'{header}': {p}" for p in line.problems(client)]
        if line.needs_human_review:
            problems.append(f"'{header}': tick 'Reviewed' once you have checked this {line.origin.upper()} suggestion")
    if not any(l.role == "amount" for l in lines):
        problems.append("at least one column must be mapped to a journal line")
    for role in ("pay_date",):
        if sum(1 for l in lines if l.role == role) > 1:
            problems.append("only one column can be the pay date")
    return problems


def save_draft(conn, user, job, client, report, form) -> list[MappingLine]:
    draft = draft_for(conn, job)
    if draft is None or draft["status"] != "draft":
        raise WorkflowError("There is no editable draft mapping for this job.")
    lines = lines_from_form(form, mp.lines_of(draft), client)
    mp.save_draft(conn, draft["id"], lines)
    audit.record(conn, actor=user, action="mapping_saved", client_id=client.id, job_id=job["id"], file_sha256=job["file_sha256"],
                 details={"draft_id": draft["id"], "lines": len(lines)})
    return lines


def apply_suggestion(conn, user, job, client, report, suggestion) -> int:
    """Fill ONLY the unassigned lines of the draft from a suggestion; never overwrites a person's or rule's choice."""
    draft = draft_for(conn, job)
    if draft is None or draft["status"] != "draft":
        raise WorkflowError("There is no editable draft mapping for this job.")
    current = mp.lines_of(draft)
    merged = mp.merge_missing(current, suggestion.lines)
    filled = sum(1 for a, b in zip(current, merged) if a is not b)
    mp.save_draft(conn, draft["id"], merged, source=suggestion.source, notice=suggestion.notice)
    audit.record(conn, actor=user, action="mapping_suggested", client_id=client.id, job_id=job["id"], file_sha256=job["file_sha256"],
                 details={"engine": suggestion.source, "model": suggestion.model, "lines_filled": filled,
                          "columns_redacted": suggestion.columns_redacted, "values_redacted": suggestion.values_redacted,
                          "sent_to_external_model": suggestion.source == "claude"})
    return filled


def submit_mapping(conn, user, job, client, report) -> None:
    draft = draft_for(conn, job)
    if draft is None or draft["status"] != "draft":
        raise WorkflowError("There is no draft mapping to submit.")
    lines = mp.lines_of(draft)
    problems = mapping_problems(lines, report, client)
    if problems:
        shown = "; ".join(problems[:4]) + (f"; and {len(problems) - 4} more" if len(problems) > 4 else "")
        raise WorkflowError("The mapping isn't complete yet: " + shown + ".")
    mp.submit(conn, draft["id"], user["email"])
    _update(conn, job["id"], status="mapping_submitted")
    audit.record(conn, actor=user, action="mapping_submitted", client_id=client.id, job_id=job["id"], file_sha256=job["file_sha256"],
                 details={"draft_id": draft["id"], "source": draft["source"]})


def approve_mapping(conn, user, job, client) -> int:
    draft = draft_for(conn, job)
    if draft is None or draft["status"] != "submitted":
        raise WorkflowError("There is no submitted mapping waiting for approval.")
    _different_people(user, {draft["created_by"], draft["submitted_by"]}, "mapping")
    version = mp.approve(conn, draft["id"], user["email"])
    _update(conn, job["id"], mapping_id=draft["id"], draft_mapping_id=None, status="ready", je_hash=None)
    audit.record(conn, actor=user, action="mapping_approved", client_id=client.id, job_id=job["id"], mapping_version=version,
                 file_sha256=job["file_sha256"], details={"draft_id": draft["id"], "proposed_by": draft["created_by"],
                                                           "source": draft["source"]})
    return version


def reject_mapping(conn, user, job, client, note: str) -> None:
    draft = draft_for(conn, job)
    if draft is None or draft["status"] != "submitted":
        raise WorkflowError("There is no submitted mapping to reject.")
    _different_people(user, {draft["created_by"], draft["submitted_by"]}, "mapping")
    mp.reject(conn, draft["id"], user["email"], note)
    _update(conn, job["id"], status="needs_mapping")
    audit.record(conn, actor=user, action="mapping_rejected", client_id=client.id, job_id=job["id"], file_sha256=job["file_sha256"],
                 details={"draft_id": draft["id"], "note": note[:200]})


def reopen_mapping(conn, user, job, client) -> None:
    draft = draft_for(conn, job)
    if draft is None or draft["status"] not in ("rejected", "submitted"):
        raise WorkflowError("There is nothing to reopen.")
    mp.reopen(conn, draft["id"])
    _update(conn, job["id"], status="needs_mapping" if not job["mapping_id"] else "ready")
    audit.record(conn, actor=user, action="mapping_reopened", client_id=client.id, job_id=job["id"], details={"draft_id": draft["id"]})


def propose_changes(conn, user, job, client, report) -> int:
    """Start a new draft (a future version) from the approved mapping this job currently uses."""
    approved = mp.get_mapping(conn, job["mapping_id"])
    if approved is None:
        raise WorkflowError("This job has no approved mapping to change.")
    if job["status"] != "ready":
        raise WorkflowError("A mapping can only be changed before the export stage.")
    lines = [MappingLine.from_dict({**l.to_dict(), "origin": "saved", "reviewed": True}) for l in mp.lines_of(approved)]
    draft_id = mp.create_draft(conn, job_id=job["id"], client_id=client.id, report_type=job["report_type"],
                               signature=job["layout_signature"], headers=report.headers, lines=lines, source="manual",
                               notice=f"Changes proposed to approved mapping v{approved['version']}.", user_email=user["email"])
    _update(conn, job["id"], draft_mapping_id=draft_id)
    audit.record(conn, actor=user, action="mapping_change_proposed", client_id=client.id, job_id=job["id"],
                 mapping_version=approved["version"], details={"draft_id": draft_id})
    return draft_id


def discard_draft(conn, user, job, client) -> None:
    if not job["mapping_id"]:
        raise WorkflowError("There is no approved mapping to fall back to; edit the draft instead.")
    draft = draft_for(conn, job)
    if draft is not None:
        mp.reopen(conn, draft["id"])
    _update(conn, job["id"], draft_mapping_id=None, status="ready")
    audit.record(conn, actor=user, action="mapping_draft_discarded", client_id=client.id, job_id=job["id"])


# ------------------------------------------------------------------ step 4: preview
@dataclass
class Preview:
    client: ClientConfig
    report: ParsedReport
    mapping_row: sqlite3.Row
    lines: list[MappingLine]
    journal: DraftJournal
    checks: list[CheckResult]
    tie_rows: list[TieOutRow]

    @property
    def ok(self) -> bool:
        return all_passed(self.checks)


def build_preview(conn: sqlite3.Connection, settings: Settings, job: sqlite3.Row) -> Preview:
    row = mp.get_mapping(conn, job["mapping_id"])
    if row is None or row["status"] != "approved":
        raise WorkflowError("An approved mapping is required before a journal can be previewed.", 409)
    client = load_client(conn, job["client_id"])
    report = load_report(settings, job)
    lines = mp.lines_of(row)
    start, end = date.fromisoformat(job["period_start"]), date.fromisoformat(job["period_end"])
    journal = build_journal(report, lines, client, period_start=start, period_end=end, allocate=bool(job["allocate"]),
                            target=job["target_system"])
    checks, tie = run_checks(report, lines, client, journal, start, end)
    return Preview(client, report, row, lines, journal, checks, tie)


def request_export(conn, settings, user, job) -> None:
    if job["status"] != "ready":
        raise WorkflowError("Export approval can only be requested from the preview stage.")
    preview = build_preview(conn, settings, job)
    if not preview.ok:
        raise WorkflowError("Export is blocked: fix the failing checks first.")
    digest = preview.journal.content_hash()
    _update(conn, job["id"], status="export_requested", je_hash=digest, export_requested_by=user["email"], export_requested_at=now())
    audit.record(conn, actor=user, action="export_requested", client_id=job["client_id"], job_id=job["id"],
                 mapping_version=preview.mapping_row["version"], file_sha256=job["file_sha256"],
                 details={"je_hash": digest, "target": job["target_system"], "allocate": bool(job["allocate"]),
                          "lines": len(preview.journal.lines), "total": str(preview.journal.total_debits),
                          "checks": {c.id: c.status for c in preview.checks}})


# ------------------------------------------------------------------ step 5: approve + export
def approve_export(conn, settings, user, job) -> None:
    if job["status"] != "export_requested":
        raise WorkflowError("There is no export waiting for approval.")
    _different_people(user, export_preparers(job), "export")
    preview = build_preview(conn, settings, job)
    if not preview.ok:
        raise WorkflowError("Export is blocked: the checks no longer all pass.")
    digest = preview.journal.content_hash()
    if digest != job["je_hash"]:
        raise WorkflowError("The journal no longer matches what was submitted for approval. Request approval again.", 409)
    _update(conn, job["id"], status="export_approved", export_approved_by=user["email"], export_approved_at=now())
    audit.record(conn, actor=user, action="export_approved", client_id=job["client_id"], job_id=job["id"],
                 mapping_version=preview.mapping_row["version"], file_sha256=job["file_sha256"],
                 details={"je_hash": digest, "prepared_by": sorted(p for p in export_preparers(job) if p)})


def reject_export(conn, user, job, note: str) -> None:
    if job["status"] != "export_requested":
        raise WorkflowError("There is no export waiting for approval.")
    _different_people(user, export_preparers(job), "export")
    _update(conn, job["id"], status="ready", je_hash=None, export_requested_by=None, export_requested_at=None)
    audit.record(conn, actor=user, action="export_rejected", client_id=job["client_id"], job_id=job["id"],
                 file_sha256=job["file_sha256"], details={"note": note[:200]})


def generate_export(conn, settings, user, job, *, delete_after: bool) -> ExportFile:
    if job["status"] != "export_approved":
        raise WorkflowError("The export has to be approved by a Reviewer before the file can be generated.", 409)
    preview = build_preview(conn, settings, job)
    if not preview.ok:
        raise WorkflowError("Export is blocked: the checks no longer all pass.")
    if preview.journal.content_hash() != job["je_hash"]:
        raise WorkflowError("The journal no longer matches what was approved. Request approval again.", 409)
    export = export_journal(preview.journal)
    digest = sha256_hex(export.content)
    stored = store_bytes(settings.export_dir, f"job_{job['id']}", export.content, ".csv")
    _update(conn, job["id"], status="exported", exported_by=user["email"], exported_at=now(), export_name=export.filename,
            export_stored=stored, export_sha256=digest, delete_after_export=int(delete_after))
    audit.record(conn, actor=user, action="export_generated", client_id=job["client_id"], job_id=job["id"],
                 mapping_version=preview.mapping_row["version"], file_sha256=job["file_sha256"],
                 details={"target": job["target_system"], "export_file": export.filename, "export_sha256": digest,
                          "rows": export.row_count, "approved_by": job["export_approved_by"], "delete_after_export": delete_after,
                          "posted_to_external_system": False})
    if delete_after:
        delete_stored(settings.upload_dir, job["file_stored"])
        _update(conn, job["id"], file_stored=None, file_deleted_at=now(), file_delete_reason="delete_after_export")
        audit.record(conn, actor=user, action="file_deleted", client_id=job["client_id"], job_id=job["id"],
                     file_sha256=job["file_sha256"], details={"reason": "delete_after_export", "kind": "upload"})
    return export


def read_export(conn, settings, user, job) -> tuple[str, bytes]:
    if job["status"] != "exported" or not job["export_stored"]:
        raise WorkflowError("There is no export file available for this job (it may have passed the retention period).", 410)
    data = read_stored(settings.export_dir, job["export_stored"])
    if sha256_hex(data) != job["export_sha256"]:
        raise WorkflowError("The stored export file failed its integrity check.", 500)
    audit.record(conn, actor=user, action="export_downloaded", client_id=job["client_id"], job_id=job["id"],
                 details={"export_file": job["export_name"], "export_sha256": job["export_sha256"]})
    return job["export_name"], data
