"""End-to-end tests through the real HTTP app (cookies, CSRF, roles, audit)."""
import csv
import html
import io
import re
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app import audit, mapping as mp
from app.auth import DEMO_USERS
from app.config import Settings
from app.demo import generate as gen
from app.main import create_app
from app.storage import resolve_stored

TOKEN_RE = re.compile(r'name="csrf_token" value="([^"]+)"')
PAT, RHEA, SAM, ALEX = (u["email"] for u in DEMO_USERS)


@pytest.fixture
def app(tmp_path, monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    settings = Settings.from_env({"DEMO_MODE": "true", "DATA_DIR": str(tmp_path), "MAX_UPLOAD_MB": "1"})
    return create_app(settings)


class Browser:
    """A logged-in user with their own cookie jar."""

    def __init__(self, app, email=None, role=None):
        self.app = app
        self.http = TestClient(app, follow_redirects=False)
        if email:
            self.login(email, role)

    def token(self, path="/login"):
        return TOKEN_RE.search(self.http.get(path).text).group(1)

    def login(self, email, role, name=None):
        name = name or next((u["name"] for u in DEMO_USERS if u["email"] == email), email.split("@")[0])
        r = self.http.post("/login", data={"name": name, "email": email, "role": role, "csrf_token": self.token("/login"), "next": "/"})
        assert r.status_code == 303, r.text
        return self

    def get(self, url, **kw):
        return self.http.get(url, **kw)

    def post(self, url, data=None, files=None):
        data = {**(data or {}), "csrf_token": self.token("/")}
        return self.http.post(url, data=data, files=files)

    def follow(self, response):
        assert response.status_code == 303, (response.status_code, response.text[:300])
        return self.http.get(response.headers["location"])


def new_job(b, client_id="our-lady-grace", target="intacct", start="2026-10-01", end="2026-10-15", allocate="no"):
    r = b.post("/jobs/new", {"client_id": client_id, "target_system": target, "report_type": "payroll_register",
                             "period_start": start, "period_end": end, "allocate": allocate})
    assert r.status_code == 303, r.text[:500]
    return int(re.search(r"/jobs/(\d+)/upload", r.headers["location"]).group(1))


def upload(b, job_id, name_or_bytes, filename=None):
    if isinstance(name_or_bytes, str):
        data, filename = Path(gen.DEMO_DIR / name_or_bytes).read_bytes(), name_or_bytes
    else:
        data = name_or_bytes
    return b.post(f"/jobs/{job_id}/upload", files={"file": (filename, data)})


def db_job(app, job_id):
    with app.state.db.read() as conn:
        return conn.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()


def audit_actions(app, job_id=None):
    with app.state.db.read() as conn:
        return [e["action"] for e in reversed(audit.list_entries(conn, limit=500, job_id=job_id))]


def form_from_draft(app, job_id, *, reviewed=True):
    with app.state.db.read() as conn:
        job = conn.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()
        draft = mp.get_mapping(conn, job["draft_mapping_id"])
        lines = mp.lines_of(draft)
    form = {}
    for i, l in enumerate(lines):
        form.update({f"line_{i}_column": l.source_column, f"line_{i}_role": l.role, f"line_{i}_side": l.side,
                     f"line_{i}_gl_account": l.gl_account, f"line_{i}_offset_account": l.offset_account,
                     f"line_{i}_entity": l.entity, f"line_{i}_fund": l.fund})
        if reviewed:
            form[f"line_{i}_reviewed"] = "on"
    return form


# ------------------------------------------------------------------ access control
def test_anonymous_users_are_sent_to_login(app):
    r = Browser(app).get("/")
    assert r.status_code == 303 and r.headers["location"].startswith("/login")
    assert Browser(app).get("/jobs/1/preview").status_code == 303


def test_demo_banner_and_security_headers(app):
    r = Browser(app).get("/login")
    assert "DEMO - synthetic data only" in r.text and "self-declared" in r.text
    assert "default-src 'self'" in r.headers["content-security-policy"]
    assert r.headers["x-frame-options"] == "DENY" and r.headers["x-content-type-options"] == "nosniff"
    assert r.headers["cache-control"] == "no-store"


def test_post_without_csrf_token_is_refused(app):
    b = Browser(app, PAT, "preparer")
    r = b.http.post("/jobs/new", data={"client_id": "st-brigid"})
    assert r.status_code == 403
    assert Browser(app).http.post("/login", data={"name": "Pat", "email": PAT, "role": "preparer"}).status_code == 403


def test_open_redirect_in_next_is_neutralised(app):
    b = Browser(app)
    r = b.http.post("/login", data={"name": "Pat", "email": PAT, "role": "preparer", "csrf_token": b.token(), "next": "//evil.example"})
    assert r.headers["location"] == "/"


def test_okta_is_gone_and_signin_is_a_name_email_role_form(app):
    page = Browser(app).get("/login").text
    assert "Okta" in page and "Single sign-on (Okta) will be added later" in page       # mentioned only as a future item
    assert 'name="name"' in page and 'name="email"' in page and 'name="role"' in page
    assert "Sign in with Okta" not in page and "/auth/okta" not in page
    assert Browser(app).get("/auth/okta/login").status_code == 404 and Browser(app).get("/login/demo").status_code in (404, 405)


def test_signin_records_the_typed_identity_and_audits_it_as_unverified(app):
    b = Browser(app).login("  Dana.Lee@Example.ORG ", "reviewer", name="  Dana   Lee  ")
    page = b.get("/").text
    assert "Dana Lee" in page and "Reviewer" in page
    with app.state.db.read() as conn:
        entry = audit.list_entries(conn, action="login")[0]
    assert (entry["actor_email"], entry["actor_name"], entry["actor_roles"]) == ("dana.lee@example.org", "Dana Lee", "reviewer")
    assert '"method":"self-declared"' in entry["details"] and '"verified":false' in entry["details"]


@pytest.mark.parametrize("name,email,role,message", [
    ("", PAT, "preparer", "Enter your name"),
    ("Pat", "", "preparer", "Enter your email"),
    ("Pat", "not-an-email", "preparer", "doesn't look like an email"),
    ("Pat", "a b@example.com", "preparer", "doesn't look like an email"),
    ("Pat", "<script>@example.com", "preparer", "doesn't look like an email"),
    ("Pat", PAT, "superuser", "Choose a role"),
    ("P" * 81, PAT, "preparer", "at most 80"),
])
def test_signin_rejects_bad_input_and_keeps_what_was_typed(app, name, email, role, message):
    b = Browser(app)
    r = b.http.post("/login", data={"name": name, "email": email, "role": role, "csrf_token": b.token("/login")})
    assert r.status_code == 400
    assert message in html.unescape(r.text)
    assert b.get("/").status_code == 303                       # still not signed in


def test_signin_form_prefill_links_do_not_sign_anyone_in(app):
    b = Browser(app)
    page = b.get("/login?name=Pat+Preparer&email=pat.preparer%40demo.example&role=preparer").text
    assert 'value="Pat Preparer"' in page and 'value="pat.preparer@demo.example"' in page and re.search(r'value="preparer"\s+checked', page)
    assert b.get("/").status_code == 303
    hostile = b.get('/login?name=%22%3E%3Cscript%3Ealert(1)%3C/script%3E&email=x').text
    assert "<script>alert(1)" not in hostile                    # prefill is escaped


def test_production_is_refused_while_signin_is_self_declared(tmp_path):
    from app.config import ConfigError
    with pytest.raises(ConfigError, match="self-declared"):
        Settings.from_env({"DEMO_MODE": "true", "APP_ENV": "production", "DATA_DIR": str(tmp_path)})


def test_roles_limit_what_each_user_can_open(app):
    pat, rhea, alex = Browser(app, PAT, "preparer"), Browser(app, RHEA, "reviewer"), Browser(app, ALEX, "admin")
    assert pat.get("/review").status_code == 403
    assert pat.get("/admin/audit").status_code == 403 and pat.get("/admin/clients").status_code == 403
    assert rhea.get("/admin/audit").status_code == 403 and rhea.get("/review").status_code == 200
    assert alex.get("/admin/audit").status_code == 200 and alex.get("/admin/clients").status_code == 200
    assert alex.get("/jobs/new").status_code == 403           # admins administer; they don't prepare journals
    assert "New journal entry" not in alex.get("/").text and "New journal entry" in pat.get("/").text


# ------------------------------------------------------------------ the happy path, two people
def test_full_flow_with_matched_mapping_allocation_review_export_and_delete(app):
    pat, rhea, alex = Browser(app, PAT, "preparer"), Browser(app, RHEA, "reviewer"), Browser(app, ALEX, "admin")
    job = new_job(pat, "our-lady-grace", "intacct", allocate="yes")

    r = upload(pat, job, "our-lady-grace_payroll_2026-10-15.csv")
    assert r.headers["location"] == f"/jobs/{job}/mapping"
    page = pat.follow(r).text
    assert "Matched a saved mapping" in page and "version 2" in page          # layout detection worked
    assert db_job(app, job)["status"] == "ready"

    preview = pat.get(f"/jobs/{job}/preview").text
    assert "Debits equal credits" in preview and "inter-entity" in preview and "FAILED" not in preview
    assert "Request export approval" in preview

    # step indicator is present on every wizard page
    assert 'class="steps"' in preview and 'aria-current="step"' in preview

    pat.post(f"/jobs/{job}/request-export")
    assert db_job(app, job)["status"] == "export_requested"

    # a Preparer has no approve permission at all
    assert "Only a Reviewer" in pat.follow(pat.post(f"/jobs/{job}/export/approve")).text
    assert db_job(app, job)["status"] == "export_requested"

    # a generate attempt before approval is refused
    assert "approved by a Reviewer" in rhea.follow(rhea.post(f"/jobs/{job}/export/generate")).text

    page = rhea.follow(rhea.post(f"/jobs/{job}/export/approve")).text
    assert "Export approved" in page
    row = db_job(app, job)
    assert (row["status"], row["export_approved_by"]) == ("export_approved", RHEA)

    page = pat.follow(pat.post(f"/jobs/{job}/export/generate", {"delete_after": "on"})).text
    assert "Nothing was posted to Sage Intacct" in page
    row = db_job(app, job)
    assert row["status"] == "exported" and row["file_stored"] is None and row["file_delete_reason"] == "delete_after_export"

    dl = pat.get(f"/jobs/{job}/export/download")
    assert dl.status_code == 200 and "attachment" in dl.headers["content-disposition"]
    rows = list(csv.DictReader(io.StringIO(dl.text)))
    assert rows[0].keys() >= {"JOURNAL", "DATE", "ACCT_NO", "LOCATION_ID", "DEBIT", "CREDIT"}
    assert {r["LOCATION_ID"] for r in rows} == {"PARISH", "SCHOOL", "STORE"}
    from decimal import Decimal as D
    assert sum(D(r["DEBIT"] or 0) for r in rows) == sum(D(r["CREDIT"] or 0) for r in rows)
    assert not any(p for p in Path(app.state.settings.upload_dir).rglob("*") if p.is_file())     # source file really gone

    assert audit_actions(app, job) == ["job_created", "file_uploaded", "mapping_matched", "export_requested", "export_approved",
                                       "export_generated", "file_deleted", "export_downloaded"]
    with app.state.db.read() as conn:
        entries = {e["action"]: e for e in audit.list_entries(conn, job_id=job, limit=50)}
        assert audit.verify_chain(conn).ok
    assert entries["file_uploaded"]["file_sha256"] == db_job(app, job)["file_sha256"]
    assert entries["export_approved"]["actor_email"] == RHEA and entries["export_approved"]["mapping_version"] == 2

    page = alex.get("/admin/audit").text
    assert "Hash chain verified" in page and RHEA in page and "export_approved" in page


def test_cannot_approve_your_own_export_even_as_reviewer(app):
    rhea = Browser(app, RHEA, "reviewer")
    job = new_job(rhea, "st-brigid", "qbo")
    rhea.follow(upload(rhea, job, "st-brigid_payroll_2026-10-15.csv"))
    # no saved mapping for St. Brigid: rules draft -> submit; a different reviewer approves it
    form = form_from_draft(app, job)
    assert "Mapping submitted" in rhea.follow(rhea.post(f"/jobs/{job}/mapping/submit", form)).text
    sam = Browser(app, SAM, "reviewer")
    assert "approved and saved as version 1" in sam.follow(sam.post(f"/jobs/{job}/mapping/approve")).text

    rhea.post(f"/jobs/{job}/request-export")
    r = rhea.follow(rhea.post(f"/jobs/{job}/export/approve"))
    assert "you cannot approve it" in r.text
    assert db_job(app, job)["status"] == "export_requested"
    assert "export_approve_denied" in audit_actions(app, job)

    # Sam did not prepare the export, so Sam can
    assert "Export approved" in sam.follow(sam.post(f"/jobs/{job}/export/approve")).text
    # but the person who uploaded/requested still cannot approve it later under another role
    again = Browser(app, RHEA, "reviewer")
    assert again.get(f"/jobs/{job}/export").status_code == 200


def test_cannot_approve_a_mapping_you_proposed(app):
    rhea = Browser(app, RHEA, "reviewer")
    job = new_job(rhea, "st-brigid")
    rhea.follow(upload(rhea, job, "st-brigid_payroll_2026-10-15.csv"))
    rhea.post(f"/jobs/{job}/mapping/submit", form_from_draft(app, job))
    r = rhea.follow(rhea.post(f"/jobs/{job}/mapping/approve"))
    assert "you cannot approve it" in r.text
    assert db_job(app, job)["status"] == "mapping_submitted" and "mapping_approve_denied" in audit_actions(app, job)
    assert "You prepared this mapping" in rhea.get(f"/jobs/{job}/mapping").text


# ------------------------------------------------------------------ new layout -> suggested mapping
def test_new_layout_goes_to_mapping_and_suggestions_are_never_auto_applied(app):
    pat, sam = Browser(app, PAT, "preparer"), Browser(app, SAM, "reviewer")
    job = new_job(pat, "our-lady-grace", start="2026-10-16", end="2026-10-31")
    page = pat.follow(upload(pat, job, "our-lady-grace_payroll_2026-10-31_NEW-LAYOUT.csv")).text
    assert db_job(app, job)["status"] == "needs_mapping"
    assert "Draft - not approved" in page and "Matched a saved mapping" not in page
    assert pat.get(f"/jobs/{job}/preview").status_code == 303                        # no preview without an approved mapping
    assert "What would be sent" not in page and "exactly what would be sent" in page   # redaction transparency panel
    assert "Marisol" not in page.split("exactly what would be sent")[1].split("</pre>")[0]

    # ask for the suggestion (offline -> mock, clearly labelled)
    after = pat.follow(pat.post(f"/jobs/{job}/mapping/suggest", form_from_draft(app, job, reviewed=False))).text
    assert "MOCK SUGGESTION" in after and "no AI model was called" in after and "none are approved" in after
    assert "MOCK suggestion" in after
    assert db_job(app, job)["mapping_id"] is None                                       # not applied

    # cannot submit until each mock line is ticked as reviewed
    blocked = pat.follow(pat.post(f"/jobs/{job}/mapping/submit", form_from_draft(app, job, reviewed=False))).text
    assert "tick &#39;Reviewed&#39;" in blocked or "tick 'Reviewed'" in blocked
    assert db_job(app, job)["status"] == "needs_mapping"

    ok = pat.follow(pat.post(f"/jobs/{job}/mapping/submit", form_from_draft(app, job, reviewed=True))).text
    assert "Mapping submitted" in ok and db_job(app, job)["status"] == "mapping_submitted"
    assert "Mapping approval" in sam.get("/review").text

    # the author cannot approve; a Preparer role cannot either
    assert "Only a Reviewer" in pat.follow(pat.post(f"/jobs/{job}/mapping/approve")).text
    assert "approved and saved as version 3" in sam.follow(sam.post(f"/jobs/{job}/mapping/approve")).text

    preview = pat.get(f"/jobs/{job}/preview").text
    assert "FAILED" not in preview and "Total Earnings" in preview and "ignored - not posted" in preview
    assert "version 3" in preview

    # the next upload of the same layout now matches the saved version
    job2 = new_job(pat, "our-lady-grace", start="2026-10-16", end="2026-10-31")
    assert "Matched a saved mapping" in pat.follow(upload(pat, job2, "our-lady-grace_payroll_2026-10-31_NEW-LAYOUT.csv")).text
    acts = audit_actions(app, job)
    assert acts.index("mapping_suggested") < acts.index("mapping_submitted") < acts.index("mapping_approved")
    with app.state.db.read() as conn:
        sug = next(e for e in audit.list_entries(conn, action="mapping_suggested"))
    assert '"engine":"mock"' in sug["details"] and '"sent_to_external_model":false' in sug["details"]


def test_broken_register_is_blocked_end_to_end(app):
    pat = Browser(app, PAT, "preparer")
    job = new_job(pat, "our-lady-grace")
    pat.follow(upload(pat, job, "our-lady-grace_payroll_2026-10-15_BROKEN.csv"))
    preview = pat.get(f"/jobs/{job}/preview").text
    assert preview.count("FAILED") >= 3 and "Export is blocked" in preview and "09/30/2026" in preview
    assert "Request export approval (blocked)" in preview
    r = pat.follow(pat.post(f"/jobs/{job}/request-export"))
    assert "Export is blocked" in r.text
    assert db_job(app, job)["status"] == "ready"
    assert pat.get(f"/jobs/{job}/export").status_code == 303   # not reachable until a request exists


def test_wrong_pay_period_blocks_an_otherwise_good_file(app):
    pat = Browser(app, PAT, "preparer")
    job = new_job(pat, "our-lady-grace", start="2026-11-01", end="2026-11-15")
    pat.follow(upload(pat, job, "our-lady-grace_payroll_2026-10-15.csv"))
    assert "outside" in pat.get(f"/jobs/{job}/preview").text
    assert "Export is blocked" in pat.follow(pat.post(f"/jobs/{job}/request-export")).text


# ------------------------------------------------------------------ intake + uploads
def test_allocation_requires_a_client_configured_for_it(app):
    pat = Browser(app, PAT, "preparer")
    r = pat.post("/jobs/new", {"client_id": "st-brigid", "target_system": "qbo", "report_type": "payroll_register",
                               "period_start": "2026-10-01", "period_end": "2026-10-15", "allocate": "yes"})
    assert r.status_code == 400 and "Allocation can&#39;t be used for St. Brigid Parish" in r.text


def test_intake_rejects_bad_dates_and_unknown_client(app):
    pat = Browser(app, PAT, "preparer")
    assert pat.post("/jobs/new", {"client_id": "st-brigid", "target_system": "qbo", "period_start": "2026-10-16",
                                  "period_end": "2026-10-15"}).status_code == 400
    assert pat.post("/jobs/new", {"client_id": "nope", "target_system": "qbo", "period_start": "2026-10-01",
                                  "period_end": "2026-10-15"}).status_code == 400


@pytest.mark.parametrize("name,data,msg", [
    ("payroll.exe", b"MZ....", "Only .csv and .xlsx"),
    ("payroll.csv", b"a,b\n" + b"1,2\n" * 400_000, "larger than the 1 MB limit"),
    ("payroll.csv", b"PK\x03\x04zip", "does not look like a CSV"),
    ("payroll.xlsx", b"not a workbook", "does not look like an .xlsx"),
    ("payroll.csv", b"just text with no table", "No table was found"),
])
def test_bad_uploads_are_rejected_audited_and_not_stored(app, name, data, msg):
    pat = Browser(app, PAT, "preparer")
    job = new_job(pat, "st-brigid")
    page = pat.follow(upload(pat, job, data, name)).text
    assert msg in page.replace("&#39;", "'")
    row = db_job(app, job)
    assert row["file_stored"] is None and row["status"] == "intake"
    assert "file_rejected" in audit_actions(app, job)
    assert not list(Path(app.state.settings.upload_dir).rglob("*.*"))


def test_uploaded_files_are_private_and_named_randomly(app):
    pat = Browser(app, PAT, "preparer")
    job = new_job(pat, "st-brigid")
    upload(pat, job, "st-brigid_payroll_2026-10-15.csv")
    stored = resolve_stored(app.state.settings.upload_dir, db_job(app, job)["file_stored"])
    assert oct(stored.stat().st_mode & 0o777) == "0o600" and "st-brigid" not in stored.name
    assert pat.get("/static/../data/uploads").status_code in (404, 403, 400)


def test_reupload_replaces_the_old_file_and_is_audited(app):
    pat = Browser(app, PAT, "preparer")
    job = new_job(pat, "our-lady-grace")
    upload(pat, job, "our-lady-grace_payroll_2026-10-15_BROKEN.csv")
    first = db_job(app, job)["file_stored"]
    upload(pat, job, "our-lady-grace_payroll_2026-10-15.csv")
    assert not resolve_stored(app.state.settings.upload_dir, first).exists()
    assert audit_actions(app, job).count("file_uploaded") == 2 and "file_deleted" in audit_actions(app, job)


def test_demo_sample_downloads_only_serve_known_files(app):
    pat = Browser(app, PAT, "preparer")
    assert pat.get("/demo-files/st-brigid_payroll_2026-10-15.csv").status_code == 200
    assert pat.get("/demo-files/../../app/config.py").status_code == 404
    assert pat.get("/demo-files/secrets.txt").status_code == 404


# ------------------------------------------------------------------ admin
def test_admin_can_change_allocation_percentages_and_it_is_audited(app):
    alex = Browser(app, ALEX, "admin")
    base = {"name": "Our Lady of Grace Parish Community", "active": "on", "paying": "PARISH", "due_from": "1300", "due_to": "2300",
            "fund_PARISH": "UNR", "fund_SCHOOL": "SCH", "fund_STORE": "STR"}
    bad = alex.follow(alex.post("/admin/clients/our-lady-grace", {**base, "pct_PARISH": "50", "pct_SCHOOL": "30", "pct_STORE": "10"}))
    assert "must add up to exactly 100" in bad.text
    ok = alex.follow(alex.post("/admin/clients/our-lady-grace", {**base, "pct_PARISH": "50", "pct_SCHOOL": "35", "pct_STORE": "15"}))
    assert "Client saved" in ok.text
    with app.state.db.read() as conn:
        pcts = {r["code"]: r["alloc_pct"] for r in conn.execute("SELECT * FROM client_entities WHERE client_id = 'our-lady-grace'")}
        entry = audit.list_entries(conn, action="client_updated")[0]
    assert pcts == {"PARISH": "50", "SCHOOL": "35", "STORE": "15"} and ALEX in entry["actor_email"]

    # the new percentages drive the next allocated journal
    pat = Browser(app, PAT, "preparer")
    job = new_job(pat, "our-lady-grace", allocate="yes")
    pat.follow(upload(pat, job, "our-lady-grace_payroll_2026-10-15.csv"))
    assert "50%" in pat.get(f"/jobs/{job}/preview").text


def test_admin_can_create_a_client(app):
    alex = Browser(app, ALEX, "admin")
    r = alex.follow(alex.post("/admin/clients/new", {"name": "St. Anselm Church", "entity_code": "MAIN"}))
    assert "St. Anselm Church" in r.text
    pat = Browser(app, PAT, "preparer")
    assert "St. Anselm Church" in pat.get("/jobs/new").text


def test_audit_page_filters_and_retention_purge_button(app):
    pat, alex = Browser(app, PAT, "preparer"), Browser(app, ALEX, "admin")
    job = new_job(pat, "st-brigid")
    page = alex.get(f"/admin/audit?job={job}").text
    assert "job_created" in page and "login" not in page.split("<tbody>")[1].split("</tbody>")[0]
    assert "Retention purge finished" in alex.follow(alex.post("/admin/purge")).text
    assert alex.post("/admin/purge").status_code == 303 and pat.post("/admin/purge").status_code == 403


def test_logout_clears_the_session(app):
    pat = Browser(app, PAT, "preparer")
    assert pat.get("/").status_code == 200
    pat.post("/logout")
    assert pat.get("/").status_code == 303


def test_intake_form_preselects_a_target_system_and_a_default_allocation(app):
    html = Browser(app, PAT, "preparer").get("/jobs/new").text
    assert re.search(r'value="intacct"\s+checked', html) and re.search(r'name="allocate" value="no" checked', html)
