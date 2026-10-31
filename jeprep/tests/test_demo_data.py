"""The synthetic demo files must behave the way the demo script says they do."""
from datetime import date
from decimal import Decimal

import pytest

from app import mapping as mp
from app.db import Database
from app.demo import generate as gen
from app.demo.seed import demo_clients, seed_demo
from app.domain import load_client
from app.journal import build_journal
from app.parsing import parse_report
from app.rules import propose_from_rules
from app.suggest import suggest_mapping
from app.validation import all_passed, run_checks

D = Decimal
CLIENTS = {c.id: c for c in demo_clients()}


def parse(name):
    data = gen.sample_bytes()[name]
    return parse_report(data, ".xlsx" if name.endswith(".xlsx") else ".csv")


def checks_for(report, lines, client, *, allocate=False, start=date(2026, 10, 1), end=date(2026, 10, 15)):
    journal = build_journal(report, lines, client, period_start=start, period_end=end, allocate=allocate, target="intacct")
    checks, tie = run_checks(report, lines, client, journal, start, end)
    return journal, {c.id: c for c in checks}, tie


def test_files_are_deterministic():
    assert gen.sample_bytes()["our-lady-grace_payroll_2026-10-15.csv"] == gen.standard_csv("our-lady-grace")
    assert gen.standard_csv("st-brigid") == gen.standard_csv("st-brigid")


@pytest.mark.parametrize("name,client_id", [
    ("st-brigid_payroll_2026-10-15.csv", "st-brigid"),
    ("holy-cross-school_payroll_2026-10-15.xlsx", "holy-cross-school"),
    ("our-lady-grace_payroll_2026-10-15.csv", "our-lady-grace"),
])
def test_standard_registers_map_by_rules_and_pass_every_check(name, client_id):
    report, client = parse(name), CLIENTS[client_id]
    lines = propose_from_rules(report, client)
    assert all(l.role for l in lines), [l.source_column for l in lines if not l.role]
    journal, checks, _ = checks_for(report, lines, client)
    assert all_passed(list(checks.values())), {k: v.detail for k, v in checks.items() if not v.passed}
    assert checks["totals_tie"].status == "pass"          # xlsx and csv both carry a totals row that agrees
    assert report.stated_total("Net Pay") is not None


def test_xlsx_sample_has_title_rows_and_real_dates():
    report = parse("holy-cross-school_payroll_2026-10-15.xlsx")
    assert report.title_lines and report.headers == gen.STANDARD_HEADERS
    assert report.row_count == 14


def test_our_lady_allocation_balances_each_entity():
    report, client = parse("our-lady-grace_payroll_2026-10-15.csv"), CLIENTS["our-lady-grace"]
    lines = propose_from_rules(report, client)
    journal, checks, _ = checks_for(report, lines, client, allocate=True)
    assert all_passed(list(checks.values()))
    assert {l.entity for l in journal.lines} == {"PARISH", "SCHOOL", "STORE"}
    assert any(l.kind == "interco" for l in journal.lines)
    salary_total = sum(l.debit for l in journal.lines if l.account_no == "6010")
    assert salary_total == report.column_total("Gross Wages")


def test_new_layout_is_not_recognised_by_rules_but_mock_suggestion_balances(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    report, client = parse("our-lady-grace_payroll_2026-10-31_NEW-LAYOUT.csv"), CLIENTS["our-lady-grace"]
    rules = propose_from_rules(report, client)
    assert [l.source_column for l in rules if l.role] == ["Worker ID", "Cost Centre", "Check Date"]   # only metadata recognised
    suggestion = suggest_mapping(report, client)
    assert suggestion.source == "mock" and all(l.role for l in suggestion.lines)
    by_col = {l.source_column: l for l in suggestion.lines}
    assert by_col["Total Earnings"].role == "ignore"                                  # subtotal: not double counted
    assert by_col["Clergy Housing Allowance"].gl_account == "6015"
    start, end = date(2026, 10, 16), date(2026, 10, 31)
    for allocate in (False, True):
        _, checks, _ = checks_for(report, suggestion.lines, client, allocate=allocate, start=start, end=end)
        assert all_passed(list(checks.values())), {k: v.detail for k, v in checks.items() if not v.passed}


def test_mock_suggestion_that_posts_the_subtotal_is_caught_by_validation(monkeypatch):
    """If a human 'fixes' Total Earnings into a debit, double counting must not slip through."""
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    report, client = parse("our-lady-grace_payroll_2026-10-31_NEW-LAYOUT.csv"), CLIENTS["our-lady-grace"]
    lines = suggest_mapping(report, client).lines
    for l in lines:
        if l.source_column == "Total Earnings":
            l.role, l.line_type, l.side, l.gl_account, l.entity, l.fund = "amount", "expense", "debit", "6010", "PARISH", "UNR"
    _, checks, _ = checks_for(report, lines, client, start=date(2026, 10, 16), end=date(2026, 10, 31))
    assert checks["balanced"].status == "fail"


def test_broken_register_is_blocked_by_the_checks_the_demo_promises():
    report, client = parse("our-lady-grace_payroll_2026-10-15_BROKEN.csv"), CLIENTS["our-lady-grace"]
    _, checks, _ = checks_for(report, propose_from_rules(report, client), client)
    assert checks["balanced"].status == "fail"
    assert checks["totals_tie"].status == "fail"
    assert checks["dates"].status == "fail" and "09/30/2026" in checks["dates"].detail
    assert checks["mapping_complete"].status == "pass"        # the mapping itself is fine; the data is not


def test_seed_creates_clients_and_two_approved_mapping_versions(tmp_path):
    db = Database(tmp_path / "demo.sqlite3")
    db.init_schema()
    assert seed_demo(db) is True
    assert seed_demo(db) is False                              # idempotent
    report = parse("our-lady-grace_payroll_2026-10-15.csv")
    new_layout = parse("our-lady-grace_payroll_2026-10-31_NEW-LAYOUT.csv")
    with db.read() as conn:
        assert {r["id"] for r in conn.execute("SELECT id FROM clients")} == set(CLIENTS)
        found = mp.find_approved(conn, "our-lady-grace", "payroll_register", report.layout_signature)
        assert found["version"] == 2
        assert [r["version"] for r in mp.approved_versions(conn, "our-lady-grace", "payroll_register")] == [2, 1]
        assert mp.find_approved(conn, "our-lady-grace", "payroll_register", new_layout.layout_signature) is None
        # no mapping exists for the other two clients: they start from the rules proposal
        assert mp.approved_versions(conn, "st-brigid", "payroll_register") == []
        cfg = load_client(conn, "our-lady-grace")
        v1 = {l.source_column: l for l in mp.lines_of(mp.approved_versions(conn, "our-lady-grace", "payroll_register")[1])}
        v2 = {l.source_column: l for l in mp.lines_of(found)}
        assert (v1["Employer 403(b) Match"].gl_account, v2["Employer 403(b) Match"].gl_account) == ("6030", "6040")
    assert cfg.allocation_problems() == []
    # the saved mapping built from the DB-loaded client produces a clean, allocated journal
    lines = mp.lines_of(found)
    _, checks, _ = checks_for(report, lines, cfg, allocate=True)
    assert all_passed(list(checks.values()))
