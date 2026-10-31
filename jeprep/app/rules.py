"""Deterministic, rules-based header recognition for common payroll register layouts.

These rules are the "known mappings" path: no model involved, same input -> same output. They only
*propose* a draft; a Reviewer must still approve before any journal can be built from it. Headers
that no rule recognises are left unassigned (that is where `suggest_mapping()` can help).
"""
from __future__ import annotations

import re
from dataclasses import dataclass

from .domain import ClientConfig, MappingLine
from .parsing import ParsedReport, normalize_header


@dataclass(frozen=True)
class Rule:
    name: str
    pattern: str
    role: str
    category: str = ""          # chart-of-accounts category for the main line
    line_type: str = ""
    side: str = ""
    offset_category: str = ""   # category of the offsetting liability account, if any
    memo: str = ""


_EE = r"((ee|employee) )?"
_ER = r"(er|employer|company) "

RULES: tuple[Rule, ...] = (
    Rule("employee name", r"^((employee|emp|worker|staff|payee) )?name$|^(employee|worker|staff)$", "employee_name"),
    Rule("employee id", r"^((employee|emp|worker|staff|payee) )?(id|number|no|num)$|^ssn$", "employee_id"),
    Rule("department", r"^(dept|department|cost cent(er|re)|division)( (code|name))?$", "department"),
    Rule("pay date", r"^(pay|check|payment|paid) date$|^date paid$", "pay_date"),
    # Employer-side costs are an expense AND a liability, so they carry an offset account.
    Rule("employer payroll tax", rf"^{_ER}(fica|social security|medicare|ss|payroll tax(es)?|tax(es)?)( .*)?$",
         "amount", "payroll_tax_expense", "expense", "debit", "fica_payable", "Employer payroll taxes"),
    Rule("employer health", rf"^{_ER}(health|medical|dental|insurance|benefits?)( .*)?$",
         "amount", "benefits_expense", "expense", "debit", "health_payable", "Employer health benefits"),
    Rule("employer retirement", rf"^{_ER}(403 ?b|401 ?k|retirement|pension|match)( .*)?$",
         "amount", "retirement_expense", "expense", "debit", "retirement_payable", "Employer retirement match"),
    Rule("gross wages", r"^(gross( pay| wages| earnings| salary)?|total gross|regular (pay|wages)|salary|salaries|wages)$",
         "amount", "salary_expense", "expense", "debit", "", "Gross wages"),
    Rule("federal withholding", r"^(federal|fed|fit)( income)?( tax| w h| wh| withholding)?( withheld)?$",
         "amount", "fed_wh_payable", "liability", "credit", "", "Federal income tax withheld"),
    Rule("state withholding", r"^(state|st|sit)( income)?( tax| w h| wh| withholding)?( withheld)?$",
         "amount", "state_wh_payable", "liability", "credit", "", "State income tax withheld"),
    Rule("employee fica", rf"^{_EE}(fica|social security|medicare|ss)( tax)?$",
         "amount", "fica_payable", "liability", "credit", "", "Employee FICA withheld"),
    Rule("employee health", rf"^{_EE}(health|medical|dental|insurance)( deduction| ded| premium)?$",
         "amount", "health_payable", "liability", "credit", "", "Employee health deduction"),
    Rule("employee retirement", rf"^{_EE}(403 ?b|401 ?k|retirement|pension)( deduction| ded| contribution)?$",
         "amount", "retirement_payable", "liability", "credit", "", "Employee retirement deduction"),
    Rule("net pay", r"^(net( pay| wages| check)?|take home( pay)?)$",
         "amount", "cash", "cash", "credit", "", "Net pay disbursed"),
)
_COMPILED = [(r, re.compile(r.pattern)) for r in RULES]


def match_rule(header: str) -> Rule | None:
    norm = normalize_header(header)
    for rule, rx in _COMPILED:
        if rx.match(norm):
            return rule
    return None


def default_dimensions(client: ClientConfig) -> tuple[str, str]:
    payer = client.paying_entity
    entity = payer.code if payer else ""
    return entity, client.default_fund_for(entity)


def propose_from_rules(report: ParsedReport, client: ClientConfig) -> list[MappingLine]:
    """One MappingLine per report column; unrecognised columns come back with an empty role."""
    entity, fund = default_dimensions(client)
    lines: list[MappingLine] = []
    for header in report.headers:
        rule = match_rule(header)
        if rule is None or (rule.role == "amount" and not report.is_amount_column(header)):
            lines.append(MappingLine(header))
            continue
        if rule.role != "amount":
            lines.append(MappingLine(header, rule.role, origin="rules", rationale=f"Matched built-in rule: {rule.name}"))
            continue
        lines.append(MappingLine(
            header, "amount", rule.line_type, rule.side,
            client.account_for_category(rule.category), entity, fund,
            client.account_for_category(rule.offset_category) if rule.offset_category else "",
            rule.memo, origin="rules", rationale=f"Matched built-in rule: {rule.name}",
        ))
    return lines
