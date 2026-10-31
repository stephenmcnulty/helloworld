import random
from datetime import date
from decimal import Decimal

import pytest

from app.allocation import AllocationError, interco_lines, split_amount
from app.journal import build_journal
from app.validation import run_checks, all_passed
from tests.conftest import make_report

D = Decimal
WEIGHTS = [("PARISH", D("60")), ("SCHOOL", D("30")), ("STORE", D("10"))]
PERIOD = dict(period_start=date(2026, 10, 1), period_end=date(2026, 10, 15), target="intacct")


def test_split_exact_when_divisible():
    assert split_amount(D("1000.00"), WEIGHTS) == {"PARISH": D("600.00"), "SCHOOL": D("300.00"), "STORE": D("100.00")}


def test_split_puts_the_stray_cent_on_the_largest_remainder():
    # 100.01 -> 60.006 / 30.003 / 10.001 ; floors leave 1 cent, largest fraction (.6) is PARISH
    assert split_amount(D("100.01"), WEIGHTS) == {"PARISH": D("60.01"), "SCHOOL": D("30.00"), "STORE": D("10.00")}


def test_split_ties_broken_by_configured_order():
    thirds = [("A", D("33.33")), ("B", D("33.33")), ("C", D("33.34"))]
    parts = split_amount(D("0.01"), thirds)
    assert sum(parts.values()) == D("0.01")
    assert parts == {"A": D("0.00"), "B": D("0.00"), "C": D("0.01")}


def test_split_negative_amount_mirrors_positive():
    pos = split_amount(D("777.77"), WEIGHTS)
    neg = split_amount(D("-777.77"), WEIGHTS)
    assert {k: -v for k, v in pos.items()} == neg


def test_split_zero_percent_entity_gets_nothing():
    parts = split_amount(D("50.00"), [("A", D("100")), ("B", D("0"))])
    assert parts == {"A": D("50.00"), "B": D("0.00")}


def test_split_requires_100_percent():
    with pytest.raises(AllocationError):
        split_amount(D("10.00"), [("A", D("50")), ("B", D("40"))])
    with pytest.raises(AllocationError):
        split_amount(D("10.00"), [])


def test_split_never_loses_a_cent_property():
    rng = random.Random(7)
    for _ in range(500):
        cents = rng.randint(-10_000_000, 10_000_000)
        amount = D(cents) / 100
        a = rng.randint(0, 100)
        b = rng.randint(0, 100 - a)
        weights = [("A", D(a)), ("B", D(b)), ("C", D(100 - a - b))]
        parts = split_amount(amount, weights)
        assert sum(parts.values()) == amount
        # no part is more than one cent away from its exact share
        for code, pct in weights:
            assert abs(parts[code] - amount * pct / 100) < D("0.01")


def test_interco_lines_make_each_entity_balance():
    # School carries 300 of expense it did not pay for; Parish paid.
    lines = interco_lines({"PARISH": D("-300"), "SCHOOL": D("300")}, "PARISH", "1300", "2300")
    school = [l for l in lines if l.entity == "SCHOOL"]
    parish = [l for l in lines if l.entity == "PARISH"]
    assert (school[0].account_no, school[0].credit) == ("2300", D("300"))   # Due to Parish
    assert (parish[0].account_no, parish[0].debit) == ("1300", D("300"))    # Due from School
    assert interco_lines({"PARISH": D("0"), "SCHOOL": D("0")}, "PARISH", "1300", "2300") == []


def test_interco_handles_entity_that_paid_more_than_it_expensed():
    lines = interco_lines({"PARISH": D("50"), "SCHOOL": D("-50")}, "PARISH", "1300", "2300")
    school = [l for l in lines if l.entity == "SCHOOL"][0]
    parish = [l for l in lines if l.entity == "PARISH"][0]
    assert (school.account_no, school.debit) == ("1300", D("50"))
    assert (parish.account_no, parish.credit) == ("2300", D("50"))


def test_allocated_journal_balances_per_entity_and_in_total(multi_client, mapping):
    report = make_report()
    j = build_journal(report, mapping, multi_client, allocate=True, **PERIOD)
    for entity, (debit, credit) in j.by_entity().items():
        assert debit == credit, entity
    assert j.total_debits == j.total_credits
    interco = [l for l in j.lines if l.kind == "interco"]
    assert {l.entity for l in interco} == {"PARISH", "SCHOOL", "STORE"}
    assert {l.account_no for l in interco} == {"1300", "2300"}


def test_allocation_splits_only_expense_lines(multi_client, mapping):
    j = build_journal(make_report(), mapping, multi_client, allocate=True, **PERIOD)
    salary = [l for l in j.lines if l.account_no == "6010"]
    assert {l.entity for l in salary} == {"PARISH", "SCHOOL", "STORE"}
    assert sum(l.debit for l in salary) == D("3000.50")
    # cash and liabilities are not split: they stay on the paying entity
    assert {l.entity for l in j.lines if l.account_no in ("1010", "2100")} == {"PARISH"}
    # each split uses the entity's own fund
    assert {l.entity: l.fund for l in salary} == {"PARISH": "UNR", "SCHOOL": "SCH", "STORE": "STR"}


def test_allocation_percentages_applied_to_the_cent(multi_client, mapping):
    j = build_journal(make_report(), mapping, multi_client, allocate=True, **PERIOD)
    school = [l for l in j.lines if l.account_no == "6010" and l.entity == "SCHOOL"][0]
    assert school.debit == D("900.15")   # 30% of 3000.50


def test_allocated_journal_passes_all_checks(multi_client, mapping):
    report = make_report()
    j = build_journal(report, mapping, multi_client, allocate=True, **PERIOD)
    checks, _ = run_checks(report, mapping, multi_client, j, PERIOD["period_start"], PERIOD["period_end"])
    assert all_passed(checks), [(c.id, c.detail) for c in checks if not c.passed]


def test_without_allocation_multi_entity_client_posts_to_mapped_entity(multi_client, mapping):
    j = build_journal(make_report(), mapping, multi_client, allocate=False, **PERIOD)
    assert {l.entity for l in j.lines} == {"PARISH"}
    assert not [l for l in j.lines if l.kind == "interco"]


def test_allocation_config_problems_are_reported(multi_client):
    assert multi_client.allocation_problems() == []
    multi_client.entities[1] = type(multi_client.entities[1])("SCHOOL", "School", D("25"), False, "SCH")
    assert any("not 100%" in p for p in multi_client.allocation_problems())
