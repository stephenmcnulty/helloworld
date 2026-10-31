"""Behaviour that matters once the demo is reachable by other people: access code, throttle, probes, headers."""
import html
import re

import pytest
from fastapi.testclient import TestClient

from app import audit
from app.auth import AttemptLimiter, access_code_ok
from app.config import ConfigError, Settings
from app.main import create_app

CODE = "open-sesame-42"
TOKEN_RE = re.compile(r'name="csrf_token" value="([^"]+)"')


def make_app(tmp_path, **env):
    return create_app(Settings.from_env({"DEMO_MODE": "true", "DATA_DIR": str(tmp_path), **env}))


@pytest.fixture
def hosted(tmp_path, monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    return make_app(tmp_path, ACCESS_CODE=CODE)


def attempt(http, code, *, email="pat@example.org", name="Pat Preparer", role="preparer"):
    token = TOKEN_RE.search(http.get("/login").text).group(1)
    data = {"name": name, "email": email, "role": role, "csrf_token": token}
    if code is not None:
        data["access_code"] = code
    return http.post("/login", data=data)


def signed_in(http) -> bool:
    return http.get("/").status_code == 200


# ------------------------------------------------------------------ access code
def test_access_code_field_appears_only_when_configured(hosted, tmp_path):
    page = TestClient(hosted).get("/login").text
    assert 'name="access_code"' in page and 'type="password"' in page
    assert CODE not in page
    plain = TestClient(make_app(tmp_path / "plain")).get("/login").text
    assert 'name="access_code"' not in plain


@pytest.mark.parametrize("code", [None, "", "nope", CODE[:-1], CODE + "x", CODE.upper()])
def test_missing_or_wrong_code_is_refused(hosted, code):
    http = TestClient(hosted, follow_redirects=False)
    r = attempt(http, code)
    assert r.status_code == 400
    assert "access code isn't right" in html.unescape(r.text)
    assert not signed_in(http)


def test_the_attempted_code_is_never_echoed_or_logged(hosted):
    http = TestClient(hosted, follow_redirects=False)
    wrong = "hunter2-hunter2"
    r = attempt(http, wrong)
    assert wrong not in r.text and CODE not in r.text
    with hosted.state.db.read() as conn:
        rows = audit.list_entries(conn, action="login_denied")
        everything = " ".join(str(tuple(row)) for row in conn.execute("SELECT * FROM audit_log"))
    assert len(rows) == 1 and rows[0]["actor_email"] == "pat@example.org"
    assert wrong not in everything and CODE not in everything
    assert "missing or wrong access code" in rows[0]["details"]


def test_correct_code_signs_in_and_is_audited(hosted):
    http = TestClient(hosted, follow_redirects=False)
    r = attempt(http, f"  {CODE}  ")                    # stray spaces from copy/paste are tolerated
    assert r.status_code == 303 and signed_in(http)
    with hosted.state.db.read() as conn:
        entry = audit.list_entries(conn, action="login")[0]
    assert '"access_code_required":true' in entry["details"] and '"verified":false' in entry["details"]


def test_the_code_still_guards_everything_else(hosted):
    http = TestClient(hosted, follow_redirects=False)
    for path in ("/", "/jobs/new", "/review", "/admin/audit", "/demo-files/st-brigid_payroll_2026-10-15.csv"):
        assert http.get(path).status_code == 303, path


def test_valid_name_email_role_are_still_required_with_the_right_code(hosted):
    http = TestClient(hosted, follow_redirects=False)
    assert attempt(http, CODE, email="not-an-email").status_code == 400 and not signed_in(http)


# ------------------------------------------------------------------ throttle
class FakeClock:
    def __init__(self):
        self.now = 1000.0

    def __call__(self):
        return self.now


def test_limiter_blocks_after_max_failures_and_recovers_after_the_window():
    clock = FakeClock()
    lim = AttemptLimiter(max_failures=3, window_seconds=60, clock=clock)
    for _ in range(3):
        assert not lim.blocked("a")
        lim.record_failure("a")
    assert lim.blocked("a") and not lim.blocked("someone-else")
    clock.now += 61
    assert not lim.blocked("a")


def test_limiter_failures_age_out_individually_and_reset_clears():
    clock = FakeClock()
    lim = AttemptLimiter(max_failures=3, window_seconds=60, clock=clock)
    lim.record_failure("a"); clock.now += 40; lim.record_failure("a"); lim.record_failure("a")
    assert lim.blocked("a")
    clock.now += 25                    # the first failure is now 65s old and drops out
    assert not lim.blocked("a")
    lim.record_failure("a"); assert lim.blocked("a")
    lim.reset("a"); assert not lim.blocked("a")


def test_too_many_wrong_codes_locks_out_even_the_right_code_for_a_while(hosted):
    clock = FakeClock()
    hosted.state.limiter = AttemptLimiter(max_failures=10, window_seconds=300, clock=clock)
    http = TestClient(hosted, follow_redirects=False)
    for _ in range(10):
        assert attempt(http, "wrong-code-0").status_code == 400
    locked = attempt(http, CODE)
    assert locked.status_code == 429 and "Too many wrong access codes" in locked.text and not signed_in(http)
    clock.now += 301
    assert attempt(http, CODE).status_code == 303 and signed_in(http)
    with hosted.state.db.read() as conn:     # lockout responses don't flood the audit log
        assert len(audit.list_entries(conn, action="login_denied")) == 10


def test_a_correct_login_clears_earlier_failures(hosted):
    http = TestClient(hosted, follow_redirects=False)
    for _ in range(5):
        attempt(http, "wrong-code-0")
    assert attempt(http, CODE).status_code == 303
    assert not hosted.state.limiter.blocked("testclient")


def test_access_code_compare_is_exact_and_needs_a_configured_code():
    assert access_code_ok(CODE, CODE) and access_code_ok(f" {CODE} ", CODE)
    assert not access_code_ok("", CODE) and not access_code_ok(CODE, "") and not access_code_ok("é" * 14, CODE)


# ------------------------------------------------------------------ config
def test_access_code_config_rules(tmp_path):
    with pytest.raises(ConfigError, match="ACCESS_CODE"):
        Settings.from_env({"ACCESS_CODE": "short", "DATA_DIR": str(tmp_path)})
    assert Settings.from_env({"ACCESS_CODE": "  longenough1 \n", "DATA_DIR": str(tmp_path)}).access_code == "longenough1"
    assert Settings.from_env({"DATA_DIR": str(tmp_path)}).access_code == ""


# ------------------------------------------------------------------ probes and headers
def test_healthz_is_open_minimal_and_sets_no_cookie(hosted):
    r = TestClient(hosted, follow_redirects=False).get("/healthz")
    assert r.status_code == 200 and r.json() == {"status": "ok"} and "set-cookie" not in r.headers


def test_search_engines_are_told_to_stay_away(hosted):
    http = TestClient(hosted, follow_redirects=False)
    robots = http.get("/robots.txt")
    assert robots.status_code == 200 and "Disallow: /" in robots.text
    assert http.get("/login").headers["x-robots-tag"] == "noindex, nofollow"


def test_hsts_only_when_served_over_https(tmp_path):
    assert "strict-transport-security" not in TestClient(make_app(tmp_path / "a")).get("/login").headers
    secure = TestClient(make_app(tmp_path / "b", COOKIE_SECURE="true")).get("/login")
    assert secure.headers["strict-transport-security"].startswith("max-age=")


def test_demo_prefill_links_never_contain_the_code(hosted):
    page = TestClient(hosted).get("/login").text
    assert "access_code" not in "".join(re.findall(r'href="(/login\?[^"]*)"', page))


def test_session_cookie_is_httponly_samesite_and_secure_when_https(tmp_path):
    secure = TestClient(make_app(tmp_path / "s", COOKIE_SECURE="true")).get("/login").headers["set-cookie"].lower()
    assert "httponly" in secure and "samesite=lax" in secure and "secure" in secure.replace("httponly", "")
    plain = TestClient(make_app(tmp_path / "p")).get("/login").headers["set-cookie"].lower()
    assert "httponly" in plain and "samesite=lax" in plain and "; secure" not in plain
