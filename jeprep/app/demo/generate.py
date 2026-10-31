"""Synthetic sample payroll registers. Every name, ID and amount is randomly generated (fixed seed) -
no real person, parish or school is represented. Run `python -m app.demo.generate` to rewrite the files.
"""
from __future__ import annotations

import csv
import io
import random
from dataclasses import dataclass
from datetime import date
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

import openpyxl

from ..config import BASE_DIR

DEMO_DIR = BASE_DIR / "demo_data"
CENT = Decimal("0.01")

FIRST = ["Marisol", "Tobias", "Imani", "Callum", "Priya", "Desmond", "Anneliese", "Rafael", "Wren", "Kofi", "Liesel", "Mateo",
         "Soraya", "Gideon", "Odalys", "Bram", "Noor", "Thaddeus", "Yara", "Emeric", "Delphine", "Jorin", "Saoirse", "Ludo"]
LAST = ["Quenby", "Fenwick", "Adeyemi", "Ostrander", "Valcourt", "Brightwater", "Nakamura", "Halloran", "Pemberton", "Ruiz",
        "Castellane", "Okonkwo", "Lindqvist", "Marchetti", "Thornbury", "Abernathy", "Delacroix", "Kowalczyk", "Sandoval", "Vance"]

STANDARD_HEADERS = ["Employee ID", "Employee Name", "Department", "Pay Date", "Gross Wages", "Employer FICA", "Employer Health",
                    "Employer 403(b) Match", "Federal Withholding", "State Withholding", "Employee FICA", "Employee Health",
                    "Employee 403(b)", "Net Pay"]
NEW_LAYOUT_HEADERS = ["Worker ID", "Legal Name", "Cost Centre", "Check Date", "Base Comp", "Clergy Housing Allowance",
                      "Total Earnings", "Statutory Deductions - Fed", "Statutory Deductions - State",
                      "Soc Sec / Medicare (Worker)", "Soc Sec / Medicare (Org)", "Group Medical (Worker)",
                      "Group Medical (Org)", "Tax-Sheltered Annuity (Worker)", "Tax-Sheltered Annuity (Org)", "Disbursed Amount"]


@dataclass(frozen=True)
class SampleFile:
    filename: str
    client_id: str
    title: str
    description: str
    period_start: date
    period_end: date


SAMPLE_FILES = [
    SampleFile("st-brigid_payroll_2026-10-15.csv", "st-brigid", "St. Brigid Parish - standard layout (CSV)",
               "Known column names, no saved mapping yet: rules propose a draft, a Reviewer approves it.",
               date(2026, 10, 1), date(2026, 10, 15)),
    SampleFile("holy-cross-school_payroll_2026-10-15.xlsx", "holy-cross-school", "Holy Cross School - Excel with title row",
               "An .xlsx register with a title line above the header and a totals row.",
               date(2026, 10, 1), date(2026, 10, 15)),
    SampleFile("our-lady-grace_payroll_2026-10-15.csv", "our-lady-grace", "Our Lady of Grace - matches the saved mapping",
               "Matches approved mapping v2, so the wizard skips straight to preview. Try it with allocation set to Yes.",
               date(2026, 10, 1), date(2026, 10, 15)),
    SampleFile("our-lady-grace_payroll_2026-10-31_NEW-LAYOUT.csv", "our-lady-grace", "Our Lady of Grace - NEW layout (AI-suggested mapping demo)",
               "A new payroll provider's column names. No saved mapping matches, so use 'Suggest a mapping'.",
               date(2026, 10, 16), date(2026, 10, 31)),
    SampleFile("our-lady-grace_payroll_2026-10-15_BROKEN.csv", "our-lady-grace", "Our Lady of Grace - deliberately broken (blocked export demo)",
               "One row is dated 09/30 and one net pay is $25 too high: validation fails and export is blocked.",
               date(2026, 10, 1), date(2026, 10, 15)),
]


def c(value) -> Decimal:
    return Decimal(value).quantize(CENT, rounding=ROUND_HALF_UP)


@dataclass
class Employee:
    emp_id: str
    name: str
    dept: str
    annual: Decimal
    clergy: bool
    health_ee: Decimal
    health_er: Decimal
    k_pct: Decimal


@dataclass
class Pay:
    base: Decimal
    housing: Decimal
    gross: Decimal
    fica_er: Decimal
    health_er: Decimal
    k_er: Decimal
    fed: Decimal
    state: Decimal
    fica_ee: Decimal
    health_ee: Decimal
    k_ee: Decimal
    net: Decimal


def make_employees(seed: int, prefix: str, depts: list[tuple[str, int, int, int]], clergy_in: str | None = None) -> list[Employee]:
    """depts: (name, count, min_salary, max_salary)."""
    rng = random.Random(seed)
    firsts, lasts = FIRST[:], LAST[:]
    rng.shuffle(firsts)
    rng.shuffle(lasts)
    employees: list[Employee] = []
    n = 0
    for dept, count, lo, hi in depts:
        for k in range(count):
            n += 1
            enrolled = rng.random() < 0.7
            employees.append(Employee(
                emp_id=f"{prefix}{1000 + n}",
                name=f"{firsts[n % len(firsts)]} {lasts[(n * 7) % len(lasts)]}",
                dept=dept,
                annual=c(rng.randrange(lo, hi, 500)),
                clergy=bool(clergy_in and dept == clergy_in and k == 0),
                health_ee=c(rng.choice([62, 85, 110])) if enrolled else c(0),
                health_er=c(rng.choice([240, 310, 380])) if enrolled else c(0),
                k_pct=Decimal(rng.choice(["0", "0.03", "0.05", "0.06"])),
            ))
    return employees


def compute_pay(e: Employee) -> Pay:
    semi = c(e.annual / 24)
    housing = c(semi * Decimal("0.25")) if e.clergy else c(0)
    base = semi - housing
    gross = base + housing
    fed_rate = Decimal("0.08") + (Decimal("0.02") if e.annual > 40000 else 0) + (Decimal("0.02") if e.annual > 55000 else 0)
    fed, state = c(gross * fed_rate), c(gross * Decimal("0.035"))
    fica = c(gross * Decimal("0.0765"))
    k_ee = c(gross * e.k_pct)
    k_er = min(k_ee, c(gross * Decimal("0.03")))
    net = gross - fed - state - fica - e.health_ee - k_ee
    return Pay(base, housing, gross, fica, e.health_er, k_er, fed, state, fica, e.health_ee, k_ee, net)


def standard_row(e: Employee, p: Pay, pay_date: str) -> list[str]:
    vals = [p.gross, p.fica_er, p.health_er, p.k_er, p.fed, p.state, p.fica_ee, p.health_ee, p.k_ee, p.net]
    return [e.emp_id, e.name, e.dept, pay_date] + [f"{v:.2f}" for v in vals]


def new_layout_row(e: Employee, p: Pay, pay_date: str) -> list[str]:
    vals = [p.base, p.housing, p.gross, p.fed, p.state, p.fica_ee, p.fica_er, p.health_ee, p.health_er, p.k_ee, p.k_er, p.net]
    return [e.emp_id, e.name, e.dept, pay_date] + [f"{v:.2f}" for v in vals]


def totals_row(rows: list[list[str]], first_amount_col: int) -> list[str]:
    out = ["Totals"] + [""] * (first_amount_col - 1)
    for i in range(first_amount_col, len(rows[0])):
        out.append(f"{sum((Decimal(r[i]) for r in rows), Decimal('0')):.2f}")
    return out


def _csv(headers: list[str], rows: list[list[str]], totals: list[str]) -> bytes:
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n")
    w.writerow(headers)
    w.writerows(rows)
    w.writerow(totals)
    return buf.getvalue().encode("utf-8")


def employees_for(client_id: str) -> list[Employee]:
    if client_id == "st-brigid":
        return make_employees(11, "SB", [("Ministry", 3, 36000, 60000), ("Administration", 3, 34000, 52000), ("Maintenance", 2, 30000, 42000)],
                              clergy_in="Ministry")
    if client_id == "holy-cross-school":
        return make_employees(22, "HC", [("Faculty", 8, 41000, 68000), ("Administration", 3, 38000, 62000), ("Support Staff", 3, 26000, 36000)])
    return make_employees(33, "OG", [("Ministry", 4, 36000, 60000), ("Administration", 3, 34000, 52000), ("Faculty", 6, 41000, 66000),
                                     ("Gift Store", 3, 24000, 32000), ("Maintenance", 2, 30000, 42000)], clergy_in="Ministry")


def standard_csv(client_id: str, pay_date: str = "10/15/2026") -> bytes:
    rows = [standard_row(e, compute_pay(e), pay_date) for e in employees_for(client_id)]
    return _csv(STANDARD_HEADERS, rows, totals_row(rows, 4))


def standard_xlsx(client_id: str, title: str) -> bytes:
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Payroll Register"
    ws.append([title])
    ws.append(["Pay period 10/01/2026 - 10/15/2026 (synthetic demo data)"])
    ws.append([])
    ws.append(STANDARD_HEADERS)
    rows = [standard_row(e, compute_pay(e), "10/15/2026") for e in employees_for(client_id)]
    for r in rows:
        ws.append(r[:3] + [date(2026, 10, 15)] + [float(x) for x in r[4:]])
    ws.append([float(x) if i >= 4 else x for i, x in enumerate(totals_row(rows, 4))])
    for row in ws.iter_rows(min_row=5, max_row=ws.max_row, min_col=5, max_col=len(STANDARD_HEADERS)):
        for cell in row:
            cell.number_format = "#,##0.00"
    for row in ws.iter_rows(min_row=5, max_row=ws.max_row - 1, min_col=4, max_col=4):
        row[0].number_format = "mm/dd/yyyy"
    buf = io.BytesIO()
    wb.save(buf)
    return buf.getvalue()


def new_layout_csv(client_id: str = "our-lady-grace") -> bytes:
    rows = [new_layout_row(e, compute_pay(e), "10/31/2026") for e in employees_for(client_id)]
    return _csv(NEW_LAYOUT_HEADERS, rows, totals_row(rows, 4))


def broken_csv(client_id: str = "our-lady-grace") -> bytes:
    employees = employees_for(client_id)
    rows = [standard_row(e, compute_pay(e), "10/15/2026") for e in employees]
    totals = totals_row(rows, 4)                       # computed BEFORE the damage, like a report that was edited afterwards
    rows[3][3] = "09/30/2026"                          # pay date outside the period
    net_idx = STANDARD_HEADERS.index("Net Pay")
    rows[1][net_idx] = f"{Decimal(rows[1][net_idx]) + Decimal('25.00'):.2f}"   # net pay overstated -> out of balance
    return _csv(STANDARD_HEADERS, rows, totals)


def sample_bytes() -> dict[str, bytes]:
    return {
        "st-brigid_payroll_2026-10-15.csv": standard_csv("st-brigid"),
        "holy-cross-school_payroll_2026-10-15.xlsx": standard_xlsx("holy-cross-school", "Holy Cross School - Payroll Register"),
        "our-lady-grace_payroll_2026-10-15.csv": standard_csv("our-lady-grace"),
        "our-lady-grace_payroll_2026-10-31_NEW-LAYOUT.csv": new_layout_csv(),
        "our-lady-grace_payroll_2026-10-15_BROKEN.csv": broken_csv(),
    }


def write_samples(out_dir: Path = DEMO_DIR) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for name, data in sample_bytes().items():
        path = out_dir / name
        path.write_bytes(data)
        paths.append(path)
    return paths


if __name__ == "__main__":
    for p in write_samples():
        print("wrote", p)
