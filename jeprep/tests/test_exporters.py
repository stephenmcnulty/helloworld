import csv
import io
from datetime import date
from decimal import Decimal

import pytest

from app.exporters import (INTACCT_COLUMNS, QBO_COLUMNS, ExportBlocked, export_journal, safe_text)
from app.journal import DraftJournal, JournalLine, build_journal
from tests.conftest import make_client, make_mapping, make_report

D = Decimal


def journal(target="intacct", client=None, allocate=False):
    return build_journal(make_report(), make_mapping(), client or make_client(), period_start=date(2026, 10, 1),
                         period_end=date(2026, 10, 15), allocate=allocate, target=target)


def read(export):
    return list(csv.DictReader(io.StringIO(export.content.decode("utf-8"))))


def test_intacct_header_and_row_count():
    j = journal("intacct")
    exp = export_journal(j)
    assert exp.filename == "JE_demo-parish_20261015_intacct.csv"
    first_line = exp.content.decode().splitlines()[0]
    assert first_line.split(",") == INTACCT_COLUMNS
    rows = read(exp)
    assert len(rows) == len(j.lines) == exp.row_count


def test_intacct_amounts_dates_and_dimensions():
    rows = read(export_journal(journal("intacct")))
    gross = next(r for r in rows if r["ACCT_NO"] == "6010")
    assert gross["DATE"] == "10/15/2026"
    assert gross["DEBIT"] == "3000.50" and gross["CREDIT"] == ""
    assert gross["LOCATION_ID"] == "PARISH" and gross["CLASSID"] == "UNR"
    assert gross["LINE_NO"] == "1"
    net = next(r for r in rows if r["ACCT_NO"] == "1010")
    assert net["CREDIT"] == "2470.91" and net["DEBIT"] == ""


def test_intacct_debits_equal_credits_in_the_file():
    rows = read(export_journal(journal("intacct")))
    assert sum(D(r["DEBIT"] or "0") for r in rows) == sum(D(r["CREDIT"] or "0") for r in rows)


def test_qbo_header_and_account_naming():
    exp = export_journal(journal("qbo"))
    assert exp.content.decode().splitlines()[0].split(",") == QBO_COLUMNS
    rows = read(exp)
    assert rows[0]["Account"] == "6010 Salaries and Wages"
    assert rows[0]["Debits"] == "3000.50" and rows[0]["Credits"] == ""
    assert rows[0]["JournalDate"] == "10/15/2026"
    assert {r["JournalNo"] for r in rows} == {"PR-DEMO-20261015"}
    assert rows[0]["Location"] == "PARISH" and rows[0]["Class"] == "UNR"


def test_allocated_export_carries_entities_and_interco_lines():
    rows = read(export_journal(journal("qbo", make_client(multi=True), allocate=True)))
    assert {r["Location"] for r in rows} == {"PARISH", "SCHOOL", "STORE"}
    assert any(r["Account"].startswith("2300") and r["Location"] == "SCHOOL" for r in rows)   # Due to
    assert any(r["Account"].startswith("1300") and r["Location"] == "PARISH" for r in rows)   # Due from
    for ent in ("PARISH", "SCHOOL", "STORE"):
        dr = sum(D(r["Debits"] or "0") for r in rows if r["Location"] == ent)
        cr = sum(D(r["Credits"] or "0") for r in rows if r["Location"] == ent)
        assert dr == cr, ent


def test_amounts_always_have_two_decimals_and_no_thousands_separator():
    for r in read(export_journal(journal("intacct"))):
        for col in ("DEBIT", "CREDIT"):
            if r[col]:
                assert "," not in r[col] and len(r[col].split(".")[1]) == 2


@pytest.mark.parametrize("raw,expected", [
    ("=HYPERLINK(\"http://evil\")", "'=HYPERLINK(\"http://evil\")"),
    ("+1+1", "'+1+1"), ("-2+3", "'-2+3"), ("@SUM(A1)", "'@SUM(A1)"),
    ("Normal memo", "Normal memo"), ("line\r\nbreak\tx", "line break x"),
])
def test_safe_text_neutralises_formula_injection(raw, expected):
    assert safe_text(raw) == expected


def test_memo_with_formula_is_neutralised_in_the_file():
    j = journal("intacct")
    j.lines[0].memo = "=cmd|' /C calc'!A0"
    rows = read(export_journal(j))
    assert rows[0]["MEMO"].startswith("'=")


def test_unbalanced_journal_cannot_be_exported():
    j = journal("intacct")
    j.lines[0].debit += D("0.01")
    with pytest.raises(ExportBlocked):
        export_journal(j)


def test_empty_journal_cannot_be_exported():
    j = DraftJournal("R", date(2026, 10, 15), "d", "intacct", "Demo")
    with pytest.raises(ExportBlocked):
        export_journal(j)


def test_unknown_target_rejected():
    j = journal("intacct")
    j.target = "netsuite"
    with pytest.raises(ValueError):
        export_journal(j)


def test_content_hash_changes_when_a_line_changes():
    a, b = journal("intacct"), journal("intacct")
    assert a.content_hash() == b.content_hash()
    b.lines[0].debit += D("1.00")
    assert a.content_hash() != b.content_hash()
