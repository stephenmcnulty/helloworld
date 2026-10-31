"""Shared fixtures: small hand-built clients and registers (independent of the demo seed data)."""
from __future__ import annotations

import csv
import io
from decimal import Decimal

import pytest

from app.domain import Account, ClientConfig, Entity, MappingLine
from app.parsing import ParsedReport, parse_report

ACCOUNTS = [
    ("1010", "Cash - Payroll", "cash"),
    ("1300", "Due from Affiliates", "due_from"),
    ("2100", "Federal Income Tax Withheld", "fed_wh_payable"),
    ("2120", "FICA Payable", "fica_payable"),
    ("2300", "Due to Affiliates", "due_to"),
    ("6010", "Salaries and Wages", "salary_expense"),
    ("6020", "Payroll Taxes", "payroll_tax_expense"),
]

HEADERS = ["Employee ID", "Employee Name", "Pay Date", "Gross Wages", "Employer FICA",
           "Federal Withholding", "Employee FICA", "Net Pay"]

# gross 1000.00 / 2000.50 ; EE FICA 7.65% ; fed 10% ; net = gross - fed - eefica
ROWS = [
    ["E1", "Avery Stone", "10/15/2026", "1000.00", "76.50", "100.00", "76.50", "823.50"],
    ["E2", "Blake Rivera", "10/15/2026", "2000.50", "153.04", "200.05", "153.04", "1647.41"],
]


def csv_bytes(headers, rows, *, title=None, totals=None) -> bytes:
    buf = io.StringIO()
    w = csv.writer(buf)
    if title:
        w.writerow([title])
        w.writerow([])
    w.writerow(headers)
    w.writerows(rows)
    if totals:
        w.writerow(totals)
    return buf.getvalue().encode()


def sum_col(rows, idx) -> Decimal:
    return sum((Decimal(r[idx]) for r in rows), Decimal("0.00"))


def totals_row(rows, label="Totals"):
    return [label, "", ""] + [str(sum_col(rows, i)) for i in range(3, len(HEADERS))]


def make_client(*, multi=False) -> ClientConfig:
    cfg = ClientConfig(id="demo", name="Demo Parish", due_from_account="1300", due_to_account="2300")
    cfg.accounts = {no: Account(no, name, cat) for no, name, cat in ACCOUNTS}
    cfg.funds = {"UNR": "Unrestricted", "SCH": "School Operating", "STR": "Store Operating"}
    if multi:
        cfg.entities = [
            Entity("PARISH", "Parish", Decimal("60"), True, "UNR"),
            Entity("SCHOOL", "School", Decimal("30"), False, "SCH"),
            Entity("STORE", "Gift Store", Decimal("10"), False, "STR"),
        ]
    else:
        cfg.entities = [Entity("PARISH", "Parish", Decimal("100"), True, "UNR")]
    return cfg


def make_mapping() -> list[MappingLine]:
    def amt(col, typ, side, acct, offset="", **kw):
        return MappingLine(col, "amount", typ, side, acct, "PARISH", "UNR", offset, origin="manual", reviewed=True, **kw)

    return [
        MappingLine("Employee ID", "employee_id", origin="manual", reviewed=True),
        MappingLine("Employee Name", "employee_name", origin="manual", reviewed=True),
        MappingLine("Pay Date", "pay_date", origin="manual", reviewed=True),
        amt("Gross Wages", "expense", "debit", "6010"),
        amt("Employer FICA", "expense", "debit", "6020", offset="2120"),
        amt("Federal Withholding", "liability", "credit", "2100"),
        amt("Employee FICA", "liability", "credit", "2120"),
        amt("Net Pay", "cash", "credit", "1010"),
    ]


def make_report(rows=ROWS, *, totals=True, title=None, headers=HEADERS) -> ParsedReport:
    data = csv_bytes(headers, rows, title=title, totals=totals_row(rows) if totals else None)
    return parse_report(data, ".csv")


@pytest.fixture
def db(tmp_path):
    from app.db import Database
    from app.domain import save_client

    database = Database(tmp_path / "test.sqlite3")
    database.init_schema()
    with database.tx() as conn:
        save_client(conn, make_client(multi=True))
    return database


@pytest.fixture
def client():
    return make_client()


@pytest.fixture
def multi_client():
    return make_client(multi=True)


@pytest.fixture
def mapping():
    return make_mapping()


@pytest.fixture
def report():
    return make_report()
