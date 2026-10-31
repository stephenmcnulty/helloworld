"""Seed the demo database: three synthetic clients, their charts of accounts, and saved mappings
(two approved versions) for Our Lady of Grace's standard register layout."""
from __future__ import annotations

from dataclasses import replace
from decimal import Decimal

from .. import audit, mapping as mp
from ..db import Database
from ..domain import Account, ClientConfig, Entity, save_client
from ..parsing import parse_report
from ..rules import propose_from_rules
from .generate import DEMO_DIR, STANDARD_HEADERS, standard_csv, write_samples

PREPARER = {"email": "pat.preparer@demo.example", "name": "Pat Preparer", "roles": ["preparer"]}
REVIEWER = {"email": "rhea.reviewer@demo.example", "name": "Rhea Reviewer", "roles": ["reviewer"]}
SEED_ACTOR = {"email": "system", "name": "Demo seed", "roles": []}


def _chart(prefix_style: str, interco: bool, housing: bool) -> dict[str, Account]:
    parish = [
        ("1010", "Cash - Payroll Account", "cash"),
        ("2100", "Federal Income Tax Withheld", "fed_wh_payable"),
        ("2110", "State Income Tax Withheld", "state_wh_payable"),
        ("2120", "FICA Payable", "fica_payable"),
        ("2130", "Health Insurance Payable", "health_payable"),
        ("2140", "403(b) Retirement Payable", "retirement_payable"),
        ("6010", "Salaries and Wages", "salary_expense"),
        ("6020", "Payroll Taxes", "payroll_tax_expense"),
        ("6030", "Employee Health Benefits", "benefits_expense"),
        ("6040", "Retirement Plan Contributions", "retirement_expense"),
    ]
    school = [
        ("1000", "Cash - Payroll Account", "cash"),
        ("2010", "Federal Withholding Payable", "fed_wh_payable"),
        ("2020", "State Withholding Payable", "state_wh_payable"),
        ("2030", "FICA Payable", "fica_payable"),
        ("2040", "Health Insurance Payable", "health_payable"),
        ("2050", "Retirement Plan Payable", "retirement_payable"),
        ("5100", "Faculty and Staff Salaries", "salary_expense"),
        ("5110", "Payroll Tax Expense", "payroll_tax_expense"),
        ("5120", "Employee Benefits - Health", "benefits_expense"),
        ("5130", "Employee Benefits - Retirement", "retirement_expense"),
    ]
    rows = list(school if prefix_style == "school" else parish)
    if housing:
        rows.append(("6015", "Clergy Housing Allowance", "housing_expense"))
    if interco:
        rows += [("1300", "Due from Affiliates", "due_from"), ("2300", "Due to Affiliates", "due_to")]
    return {no: Account(no, name, cat) for no, name, cat in rows}


def demo_clients() -> list[ClientConfig]:
    return [
        ClientConfig(
            id="st-brigid", name="St. Brigid Parish", description="Single-entity parish (synthetic).",
            entities=[Entity("PARISH", "St. Brigid Parish", Decimal("100"), True, "UNR")],
            funds={"UNR": "Unrestricted - General", "RES": "Donor-Restricted"},
            accounts=_chart("parish", interco=False, housing=True),
        ),
        ClientConfig(
            id="holy-cross-school", name="Holy Cross School", description="Single-entity parish school (synthetic).",
            entities=[Entity("SCHOOL", "Holy Cross School", Decimal("100"), True, "OPS")],
            funds={"OPS": "Operating Fund", "GRANT": "Restricted - Grants"},
            accounts=_chart("school", interco=False, housing=False),
        ),
        ClientConfig(
            id="our-lady-grace", name="Our Lady of Grace Parish Community",
            description="A parish that also runs a school and a gift store (synthetic). Payroll is paid by the Parish and "
                        "allocated 60/30/10 to Parish / School / Gift Store.",
            due_from_account="1300", due_to_account="2300",
            entities=[Entity("PARISH", "Parish", Decimal("60"), True, "UNR"),
                      Entity("SCHOOL", "School", Decimal("30"), False, "SCH"),
                      Entity("STORE", "Gift Store", Decimal("10"), False, "STR")],
            funds={"UNR": "Unrestricted - General", "RES": "Donor-Restricted", "SCH": "School Operating", "STR": "Gift Store Operating"},
            accounts=_chart("parish", interco=True, housing=True),
        ),
    ]


def seed_demo(db: Database) -> bool:
    """Idempotent: does nothing if clients already exist. Returns True if it seeded."""
    with db.read() as conn:
        if conn.execute("SELECT COUNT(*) AS n FROM clients").fetchone()["n"]:
            return False
    if not DEMO_DIR.joinpath("our-lady-grace_payroll_2026-10-15.csv").exists():
        write_samples()
    clients = demo_clients()
    report = parse_report(standard_csv("our-lady-grace"), ".csv")
    cfg = next(c for c in clients if c.id == "our-lady-grace")
    base = propose_from_rules(report, cfg)
    base = [replace(l, origin="saved", reviewed=True, rationale="") for l in base]
    # v1 mapped the employer 403(b) match to the health-benefits expense account by mistake; v2 corrects it.
    v1 = [replace(l, gl_account="6030") if l.source_column == "Employer 403(b) Match" else l for l in base]

    with db.tx() as conn:
        for client in clients:
            save_client(conn, client)
            audit.record(conn, actor=SEED_ACTOR, action="client_created", client_id=client.id,
                         details={"name": client.name, "source": "demo seed (synthetic data)"})
        sig = report.layout_signature
        for lines, note in ((v1, "initial mapping"), (base, "corrected employer 403(b) match account")):
            mid = mp.create_draft(conn, job_id=None, client_id=cfg.id, report_type="payroll_register", signature=sig,
                                  headers=STANDARD_HEADERS, lines=lines, source="manual", notice=note, user_email=PREPARER["email"])
            mp.submit(conn, mid, PREPARER["email"])
            version = mp.approve(conn, mid, REVIEWER["email"])
            audit.record(conn, actor=PREPARER, action="mapping_submitted", client_id=cfg.id, details={"note": note, "seeded": True})
            audit.record(conn, actor=REVIEWER, action="mapping_approved", client_id=cfg.id, mapping_version=version,
                         details={"note": note, "seeded": True})
    return True
