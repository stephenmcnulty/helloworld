from dataclasses import replace
from datetime import date
from decimal import Decimal

from app.domain import MappingLine
from app.journal import build_journal
from app.validation import FAIL, PASS, WARN, all_passed, run_checks
from tests.conftest import HEADERS, ROWS, make_client, make_mapping, make_report

D = Decimal
START, END = date(2026, 10, 1), date(2026, 10, 15)


def run(report, mapping, client=None, *, allocate=False, start=START, end=END):
    client = client or make_client()
    journal = build_journal(report, mapping, client, period_start=start, period_end=end, allocate=allocate, target="intacct")
    checks, tie = run_checks(report, mapping, client, journal, start, end)
    return journal, {c.id: c for c in checks}, tie


def test_clean_register_passes_every_check():
    journal, checks, _ = run(make_report(), make_mapping())
    assert {c.id: c.status for c in checks.values()} == {
        "mapping_complete": PASS, "balanced": PASS, "entities_balanced": PASS, "totals_tie": PASS, "dates": PASS,
    }
    assert journal.total_debits == journal.total_credits == D("3230.04")   # 3000.50 gross + 229.54 employer FICA


def test_debits_must_equal_credits():
    rows = [r[:] for r in ROWS]
    rows[0][7] = "848.50"   # net pay overstated by 25.00, so the source does not foot
    _, checks, _ = run(make_report(rows, totals=False), make_mapping())
    assert checks["balanced"].status == FAIL
    assert "25.00" in checks["balanced"].detail


def test_unmapped_column_blocks_export():
    mapping = [m for m in make_mapping() if m.source_column != "Federal Withholding"]
    _, checks, _ = run(make_report(), mapping)
    assert checks["mapping_complete"].status == FAIL
    assert "Federal Withholding" in checks["mapping_complete"].detail


def test_amount_line_without_account_is_unmapped():
    mapping = make_mapping()
    mapping[3] = replace(mapping[3], gl_account="")
    _, checks, _ = run(make_report(), mapping)
    assert checks["mapping_complete"].status == FAIL
    assert "GL account missing" in checks["mapping_complete"].detail


def test_unassigned_role_is_unmapped():
    mapping = make_mapping()
    mapping[0] = MappingLine("Employee ID")
    _, checks, _ = run(make_report(), mapping)
    assert checks["mapping_complete"].status == FAIL
    assert "no role assigned" in checks["mapping_complete"].detail


def test_invalid_dimension_values_fail():
    mapping = make_mapping()
    mapping[3] = replace(mapping[3], entity="NOPE", fund="NOFUND", gl_account="9999")
    _, checks, _ = run(make_report(), mapping)
    detail = checks["mapping_complete"].detail
    assert checks["mapping_complete"].status == FAIL
    assert "9999" in detail


def test_totals_must_tie_to_the_reports_own_total_row():
    rows = [r[:] for r in ROWS]
    data_rows = [r[:] for r in rows]
    report = make_report(rows)
    # tamper with one employee after the totals row was computed
    report.df.loc[0, "Gross Wages"] = "1100.00"
    _, checks, tie = run(report, make_mapping())
    assert checks["totals_tie"].status == FAIL
    gross = next(r for r in tie if r.column == "Gross Wages")
    assert gross.vs_stated == D("100.00")
    assert data_rows == ROWS   # fixture untouched


def test_totals_tie_without_total_row_still_compares_journal_to_source():
    _, checks, tie = run(make_report(totals=False), make_mapping())
    assert checks["totals_tie"].status == PASS
    assert all(r.vs_journal == 0 for r in tie)
    assert "no total row" in checks["totals_tie"].detail


def test_column_missing_from_journal_does_not_tie():
    mapping = make_mapping()
    mapping[4] = replace(mapping[4], gl_account="")   # Employer FICA cannot be posted
    _, checks, tie = run(make_report(), mapping)
    assert checks["totals_tie"].status == FAIL
    assert next(r for r in tie if r.column == "Employer FICA").journal_amount == 0


def test_ignored_nonzero_column_is_a_warning_not_a_failure():
    mapping = make_mapping()
    mapping[4] = MappingLine("Employer FICA", "ignore", origin="manual", reviewed=True)
    _, checks, _ = run(make_report(), mapping)
    assert checks["totals_tie"].status == WARN
    assert "Employer FICA" in checks["totals_tie"].detail
    assert checks["balanced"].status == PASS   # employer FICA posts debit and credit together


def test_dates_outside_period_fail():
    rows = [r[:] for r in ROWS]
    rows[1][2] = "09/30/2026"
    _, checks, _ = run(make_report(rows), make_mapping())
    assert checks["dates"].status == FAIL
    assert "09/30/2026" in checks["dates"].detail


def test_unreadable_date_fails():
    rows = [r[:] for r in ROWS]
    rows[0][2] = "someday"
    _, checks, _ = run(make_report(rows), make_mapping())
    assert checks["dates"].status == FAIL


def test_period_end_before_start_fails():
    _, checks, _ = run(make_report(), make_mapping(), start=date(2026, 10, 16), end=date(2026, 10, 15))
    assert checks["dates"].status == FAIL


def test_no_pay_date_column_is_a_warning():
    mapping = [m for m in make_mapping() if m.source_column != "Pay Date"] + [MappingLine("Pay Date", "ignore")]
    _, checks, _ = run(make_report(), mapping)
    assert checks["dates"].status == WARN
    assert all_passed(list(checks.values()))


def test_entity_balance_check_catches_split_entities_without_allocation():
    client = make_client(multi=True)
    mapping = make_mapping()
    mapping[3] = replace(mapping[3], entity="SCHOOL", fund="SCH")   # salary to School, cash stays Parish
    journal, checks, _ = run(make_report(), mapping, client, allocate=False)
    assert checks["balanced"].status == PASS
    assert checks["entities_balanced"].status == FAIL
    assert "SCHOOL" in checks["entities_balanced"].detail
    assert not all_passed(list(checks.values()))


def test_negative_column_total_flips_side_and_still_ties():
    rows = [["E1", "Avery Stone", "10/15/2026", "-100.00", "0.00", "0.00", "0.00", "-100.00"]]
    report = make_report(rows)
    journal, checks, tie = run(report, make_mapping())
    salary = [l for l in journal.lines if l.account_no == "6010"][0]
    assert (salary.debit, salary.credit) == (D("0.00"), D("100.00"))   # flipped to the credit side
    assert checks["totals_tie"].status == PASS
    assert checks["balanced"].status == PASS


def test_zero_total_columns_are_skipped_not_posted():
    journal, _, _ = run(make_report([["E1", "A", "10/15/2026", "100.00", "0.00", "10.00", "0.00", "90.00"]]), make_mapping())
    assert "Employer FICA" in journal.zero_columns
    assert all(l.debit + l.credit != 0 for l in journal.lines)
