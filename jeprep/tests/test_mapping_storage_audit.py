import os
import sqlite3
import stat
import zipfile
import io
from datetime import datetime, timedelta, timezone

import pytest

from app import audit, mapping as mp
from app.config import ConfigError, Settings
from app.domain import MappingLine
from app.rules import match_rule, propose_from_rules
from app.storage import (UploadError, delete_stored, purge_expired, read_stored, resolve_stored, sanitize_filename,
                         store_bytes, validate_upload)
from tests.conftest import make_client, make_mapping, make_report

USER = {"email": "p@example.com", "name": "Pat", "roles": ["preparer"]}


# ------------------------------------------------------------------ rules
def test_rules_recognise_the_standard_headers():
    expect = {"Employee ID": "employee_id", "Employee Name": "employee_name", "Pay Date": "pay_date",
              "Gross Wages": "amount", "Employer FICA": "amount", "Federal Withholding": "amount",
              "Employee FICA": "amount", "Net Pay": "amount"}
    for header, role in expect.items():
        assert match_rule(header).role == role, header


def test_rules_leave_unfamiliar_headers_unassigned():
    for header in ["Base Comp", "Total Earnings", "Statutory Deductions - Fed", "Disbursed Amount", "Legal Name"]:
        assert match_rule(header) is None, header


def test_rule_proposals_resolve_accounts_from_the_clients_chart():
    lines = {l.source_column: l for l in propose_from_rules(make_report(), make_client())}
    gross, er = lines["Gross Wages"], lines["Employer FICA"]
    assert (gross.gl_account, gross.side, gross.line_type, gross.origin) == ("6010", "debit", "expense", "rules")
    assert (er.gl_account, er.offset_account) == ("6020", "2120")
    assert lines["Net Pay"].gl_account == "1010"
    assert gross.reviewed is False and gross.entity == "PARISH" and gross.fund == "UNR"


def test_rules_are_deterministic():
    a = propose_from_rules(make_report(), make_client())
    b = propose_from_rules(make_report(), make_client())
    assert [l.to_dict() for l in a] == [l.to_dict() for l in b]


# ------------------------------------------------------------------ mapping lifecycle
def draft(db, sig="sig-a", lines=None):
    with db.tx() as conn:
        return mp.create_draft(conn, job_id=None, client_id="demo", report_type="payroll_register", signature=sig,
                               headers=["a"], lines=lines or make_mapping(), source="manual", notice="", user_email="p@example.com")


def test_versions_increment_per_client_and_report_type(db):
    ids = [draft(db) for _ in range(2)]
    with db.tx() as conn:
        for mid in ids:
            mp.submit(conn, mid, "p@example.com")
        assert [mp.approve(conn, mid, "r@example.com") for mid in ids] == [1, 2]


def test_find_approved_matches_signature_and_returns_latest_version(db):
    a1, a2, other = draft(db, "sig-a"), draft(db, "sig-a"), draft(db, "sig-b")
    with db.tx() as conn:
        for mid in (a1, a2, other):
            mp.submit(conn, mid, "p")
            mp.approve(conn, mid, "r")
    with db.read() as conn:
        found = mp.find_approved(conn, "demo", "payroll_register", "sig-a")
        assert found["version"] == 2 and found["id"] == a2
        assert mp.find_approved(conn, "demo", "payroll_register", "sig-zzz") is None
        assert len(mp.lines_of(found)) == len(make_mapping())


def test_unapproved_mappings_are_never_found(db):
    mid = draft(db)
    with db.tx() as conn:
        mp.submit(conn, mid, "p")
    with db.read() as conn:
        assert mp.find_approved(conn, "demo", "payroll_register", "sig-a") is None


def test_cannot_approve_a_draft_or_edit_a_submitted_mapping(db):
    mid = draft(db)
    with db.tx() as conn:
        with pytest.raises(mp.MappingError):
            mp.approve(conn, mid, "r")
        mp.submit(conn, mid, "p")
        with pytest.raises(mp.MappingError):
            mp.save_draft(conn, mid, make_mapping())


def test_reject_then_reopen_then_resubmit(db):
    mid = draft(db)
    with db.tx() as conn:
        mp.submit(conn, mid, "p")
        mp.reject(conn, mid, "r", "wrong account")
        assert mp.get_mapping(conn, mid)["status"] == "rejected"
        mp.reopen(conn, mid)
        mp.submit(conn, mid, "p")
        assert mp.approve(conn, mid, "r") == 1


def test_merge_missing_only_fills_unassigned_lines():
    base = [MappingLine("A", "ignore", origin="manual"), MappingLine("B")]
    extra = [MappingLine("A", "amount", origin="ai"), MappingLine("B", "employee_name", origin="ai")]
    merged = mp.merge_missing(base, extra)
    assert [(l.role, l.origin) for l in merged] == [("ignore", "manual"), ("employee_name", "ai")]


# ------------------------------------------------------------------ audit log
def test_audit_chain_verifies_and_detects_tampering(db):
    with db.tx() as conn:
        for i in range(5):
            audit.record(conn, actor=USER, action=f"step_{i}", job_id=i, details={"n": i})
    with db.read() as conn:
        assert audit.verify_chain(conn) == audit.ChainStatus(True, 5, None)
    # the triggers refuse edits and deletes...
    with db.tx() as conn:
        with pytest.raises(sqlite3.DatabaseError, match="append-only"):
            conn.execute("UPDATE audit_log SET actor_email = 'x' WHERE id = 3")
    with db.tx() as conn:
        with pytest.raises(sqlite3.DatabaseError, match="append-only"):
            conn.execute("DELETE FROM audit_log WHERE id = 3")
    # ...and even if someone drops the trigger, the chain exposes the edit
    with db.tx() as conn:
        conn.execute("DROP TRIGGER audit_log_no_update")
        conn.execute("UPDATE audit_log SET actor_email = 'mallory@example.com' WHERE id = 3")
    with db.read() as conn:
        status = audit.verify_chain(conn)
        assert not status.ok and status.broken_at == 3


def test_audit_records_who_what_mapping_version_and_file_hash(db):
    with db.tx() as conn:
        audit.record(conn, actor={"email": "r@example.com", "name": "Rhea", "roles": ["reviewer"]}, action="export_approved",
                     client_id="demo", job_id=7, mapping_version=3, file_sha256="ab" * 32, details={"je_hash": "x"})
    with db.read() as conn:
        row = audit.list_entries(conn)[0]
    assert (row["actor_email"], row["actor_roles"], row["action"], row["mapping_version"], row["file_sha256"]) == \
           ("r@example.com", "reviewer", "export_approved", 3, "ab" * 32)
    assert row["ts"].endswith("+00:00")


# ------------------------------------------------------------------ uploads and storage
def xlsx_bytes(extra=None):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("[Content_Types].xml", "<Types/>")
        zf.writestr("xl/workbook.xml", "<workbook/>")
        for name, data in (extra or {}).items():
            zf.writestr(name, data)
    return buf.getvalue()


@pytest.mark.parametrize("name,data,msg", [
    ("report.exe", b"a,b\n1,2\n", "Only .csv and .xlsx"),
    ("report.xls", b"a,b\n", "Only .csv and .xlsx"),
    ("report.csv", b"", "empty"),
    ("report.csv", b"a,b\n" + b"x" * 200, "larger than"),
    ("report.csv", b"a,b\x00\n1,2", "does not look like a CSV"),
    ("report.csv", b"PK\x03\x04zipdata", "does not look like a CSV"),
    ("report.csv", b"%PDF-1.7 ...", "does not look like a CSV"),
    ("report.xlsx", b"a,b\n1,2\n", "does not look like an .xlsx"),
    ("report.xlsx", b"PK\x03\x04garbage", "does not look like an .xlsx"),
])
def test_invalid_uploads_are_rejected(name, data, msg):
    with pytest.raises(UploadError, match=msg):
        validate_upload(name, data, max_bytes=100)


def test_macro_and_path_traversal_workbooks_are_rejected():
    with pytest.raises(UploadError, match="macros"):
        validate_upload("a.xlsx", xlsx_bytes({"xl/vbaProject.bin": b"x"}), 10_000)
    with pytest.raises(UploadError, match="unsafe paths"):
        validate_upload("a.xlsx", xlsx_bytes({"../evil.xml": b"x"}), 10_000)


def test_valid_uploads_pass():
    assert validate_upload("Payroll.CSV", b"a,b\n1,2\n", 1000) == ".csv"
    assert validate_upload("p.xlsx", xlsx_bytes(), 10_000) == ".xlsx"


def test_filename_sanitising():
    assert sanitize_filename("../../etc/passwd") == "passwd"
    assert sanitize_filename("C:\\temp\\pay\x00roll.csv") == "payroll.csv"
    assert sanitize_filename("") == "upload"
    assert len(sanitize_filename("a" * 500 + ".csv")) <= 120


def test_stored_files_are_private_randomly_named_and_confined(tmp_path):
    stored = store_bytes(tmp_path / "uploads", "job_1", b"secret", ".csv")
    path = resolve_stored(tmp_path / "uploads", stored)
    assert stat.S_IMODE(path.stat().st_mode) == 0o600
    assert stat.S_IMODE(path.parent.stat().st_mode) == 0o700
    assert "payroll" not in stored and stored.endswith(".csv")
    assert read_stored(tmp_path / "uploads", stored) == b"secret"
    with pytest.raises(UploadError):
        resolve_stored(tmp_path / "uploads", "../../etc/passwd")
    assert delete_stored(tmp_path / "uploads", stored) is True
    assert not path.exists() and not path.parent.exists()
    assert delete_stored(tmp_path / "uploads", stored) is False


def test_retention_purge_deletes_only_expired_files_and_audits_it(db, tmp_path):
    settings = Settings.from_env({"DEMO_MODE": "true", "DATA_DIR": str(tmp_path), "UPLOAD_RETENTION_DAYS": "30"})
    now = datetime.now(timezone.utc)
    old = (now - timedelta(days=45)).isoformat(timespec="seconds")
    fresh = (now - timedelta(days=2)).isoformat(timespec="seconds")
    with db.tx() as conn:
        for jid, ts in ((1, old), (2, fresh)):
            stored = store_bytes(settings.upload_dir, f"job_{jid}", b"data", ".csv")
            conn.execute(
                """INSERT INTO jobs (id, client_id, target_system, report_type, period_start, period_end, status, created_by,
                   created_by_name, created_at, updated_at, file_stored, file_sha256, file_uploaded_at)
                   VALUES (?, 'demo', 'qbo', 'payroll_register', '2026-10-01', '2026-10-15', 'ready', 'p', 'P', ?, ?, ?, 'h', ?)""",
                (jid, ts, ts, stored, ts))
    removed = purge_expired(settings, db)
    assert removed == [{"job_id": 1, "kind": "upload"}]
    with db.read() as conn:
        j1 = conn.execute("SELECT * FROM jobs WHERE id = 1").fetchone()
        j2 = conn.execute("SELECT * FROM jobs WHERE id = 2").fetchone()
        assert j1["file_stored"] is None and j1["file_delete_reason"] == "retention"
        assert j2["file_stored"] is not None and resolve_stored(settings.upload_dir, j2["file_stored"]).exists()
        assert audit.list_entries(conn, action="file_deleted")[0]["job_id"] == 1


# ------------------------------------------------------------------ config safety
def test_config_refuses_unsafe_setups(tmp_path):
    with pytest.raises(ConfigError, match="not configured"):
        Settings.from_env({"DATA_DIR": str(tmp_path)})
    with pytest.raises(ConfigError, match="not allowed"):
        Settings.from_env({"DEMO_MODE": "true", "APP_ENV": "production", "DATA_DIR": str(tmp_path)})
    with pytest.raises(ConfigError, match="SECRET_KEY"):
        Settings.from_env({"OKTA_ISSUER": "https://x.okta.com", "OKTA_CLIENT_ID": "a", "OKTA_CLIENT_SECRET": "b",
                           "DATA_DIR": str(tmp_path)})
    ok = Settings.from_env({"DEMO_MODE": "true", "DATA_DIR": str(tmp_path)})
    assert ok.demo_mode and len(ok.secret_key) >= 32
    okta = Settings.from_env({"OKTA_ISSUER": "https://x.okta.com/", "OKTA_CLIENT_ID": "a", "OKTA_CLIENT_SECRET": "b",
                              "SECRET_KEY": "k" * 40, "DATA_DIR": str(tmp_path)})
    assert okta.okta_configured and okta.okta_issuer == "https://x.okta.com" and not okta.demo_mode
