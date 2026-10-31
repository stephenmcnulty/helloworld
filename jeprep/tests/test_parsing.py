import io
from decimal import Decimal

import openpyxl
import pytest

from app.money import parse_date, parse_money
from app.parsing import ParseError, layout_signature, parse_report
from tests.conftest import HEADERS, ROWS, csv_bytes, make_report, totals_row

D = Decimal


@pytest.mark.parametrize("raw,expected", [
    ("1234.5", D("1234.50")), ("$1,234.56", D("1234.56")), ("(12.00)", D("-12.00")), ("-5", D("-5.00")),
    ("12-", D("-12.00")), ("0", D("0.00")), (" 7 ", D("7.00")), (".5", D("0.50")),
])
def test_parse_money_accepts_common_formats(raw, expected):
    assert parse_money(raw) == expected


@pytest.mark.parametrize("raw", ["", "abc", "1e5", "NaN", "Infinity", "10/15/2026", "1.2.3", "E1001", None, "9" * 30])
def test_parse_money_rejects_non_money(raw):
    assert parse_money(raw) is None


@pytest.mark.parametrize("raw", ["2026-10-15", "10/15/2026", "10/15/26", "2026-10-15 00:00:00", "Oct 15, 2026"])
def test_parse_date_formats(raw):
    assert parse_date(raw).isoformat() == "2026-10-15"


def test_parse_date_rejects_garbage():
    assert parse_date("soon") is None and parse_date("") is None


def test_csv_report_basics(report):
    assert report.headers == HEADERS
    assert report.row_count == 2
    assert report.column_total("Gross Wages") == D("3000.50")
    assert report.stated_total("Gross Wages") == D("3000.50")
    assert "Gross Wages" in report.amount_columns()
    assert "Employee Name" not in report.amount_columns()


def test_title_lines_above_header_are_skipped():
    report = make_report(title="St. Brigid Parish - Payroll Register")
    assert report.headers == HEADERS
    assert report.title_lines == ["St. Brigid Parish - Payroll Register"]


def test_totals_row_is_not_counted_as_data():
    report = make_report(totals=True)
    assert report.row_count == 2 and report.totals_row is not None
    assert report.column_total("Net Pay") == D("2470.91")


def test_subtotal_rows_are_ignored():
    data = csv_bytes(HEADERS, ROWS[:1] + [["Subtotal", "", "", "1.00", "1.00", "1.00", "1.00", "1.00"]] + ROWS[1:])
    report = parse_report(data, ".csv")
    assert report.row_count == 2 and report.skipped_rows == 1


def test_duplicate_and_blank_headers_are_made_unique():
    data = b"A,A,,B\n1,2,x,3\n"
    report = parse_report(data, ".csv")
    assert report.headers == ["A", "A (2)", "Column 3", "B"]


def test_layout_signature_ignores_order_case_and_punctuation():
    assert layout_signature(["Gross Wages", "Net Pay"]) == layout_signature(["net  pay", "GROSS-WAGES"])
    assert layout_signature(["Gross Wages", "Net Pay"]) != layout_signature(["Gross Wages", "Net Pay", "Bonus"])


def test_header_without_rows_is_an_error():
    with pytest.raises(ParseError):
        parse_report(b"A,B,C\n", ".csv")


def test_no_table_is_an_error():
    with pytest.raises(ParseError):
        parse_report(b"just one lonely cell\n", ".csv")


def test_row_limit_enforced():
    body = "A,B\n" + "\n".join(f"x{i},{i}" for i in range(200))
    with pytest.raises(ParseError):
        parse_report(body.encode(), ".csv", max_rows=100)


def test_column_limit_enforced():
    wide = ",".join(f"c{i}" for i in range(30)) + "\n" + ",".join("1" for _ in range(30)) + "\n"
    with pytest.raises(ParseError):
        parse_report(wide.encode(), ".csv", max_columns=10)


def test_cp1252_csv_is_decoded():
    data = "Name,Amount\nJosé Muñoz,10.00\n".encode("cp1252")
    assert parse_report(data, ".csv").values("Name") == ["José Muñoz"]


def test_xlsx_roundtrip_with_title_rows_and_numeric_cells():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(["Holy Cross School - Payroll Register"])
    ws.append([])
    ws.append(HEADERS)
    for r in ROWS:
        ws.append([r[0], r[1], r[2]] + [float(x) for x in r[3:]])
    ws.append(totals_row(ROWS))
    buf = io.BytesIO()
    wb.save(buf)
    report = parse_report(buf.getvalue(), ".xlsx")
    assert report.headers == HEADERS
    assert report.title_lines == ["Holy Cross School - Payroll Register"]
    assert report.column_total("Gross Wages") == D("3000.50")
    assert report.stated_total("Net Pay") == D("2470.91")


def test_corrupt_xlsx_gives_a_safe_error():
    with pytest.raises(ParseError) as exc:
        parse_report(b"PK\x03\x04 not really", ".xlsx")
    assert "Excel file could not be read" in str(exc.value)
