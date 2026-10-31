"""suggest_mapping(): propose a mapping for an unfamiliar report layout.

* With ANTHROPIC_API_KEY set, asks Claude - but only ever sends redacted headers + a few redacted
  sample rows (see redaction.py) plus the client's chart of accounts / entities / funds.
* Without a key (or if the call fails), falls back to a *mock* keyword heuristic that is labelled as
  such everywhere it is shown, so the demo runs offline.
* The result is only ever a proposal. Nothing here writes to the database or approves anything.
"""
from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any

from .domain import LINE_TYPES, ROLES, SIDES, ClientConfig, MappingLine
from .money import parse_money
from .parsing import ParsedReport, normalize_header
from .redaction import RedactionResult, build_model_payload, restore
from .rules import default_dimensions

DEFAULT_MODEL = "claude-opus-5-5"
MOCK_LABEL = "MOCK SUGGESTION - no AI model was called (ANTHROPIC_API_KEY is not set). Built-in keyword heuristic, for demo only."

SYSTEM_PROMPT = """You help an accounting firm turn a payroll register into a journal entry.
You are given the column headers of an unfamiliar payroll register, a few sample rows (employee names
and IDs are replaced by tokens such as EMP_001 - treat them as opaque), and the client's chart of accounts,
entities and funds. For EVERY column, decide its role and, for money columns, how it should post.

Rules:
- role "amount": a column whose total becomes a journal line. Set line_type (expense, liability, cash, asset, other),
  side (debit or credit), gl_account (must be one of the provided account numbers), entity and fund (from the provided lists).
- Employer-side costs (employer taxes, employer benefits, employer retirement match) are an expense (debit) and ALSO a
  liability: set offset_account to the matching payable account.
- Employee withholdings and deductions are liabilities (credit). Net pay / amount disbursed is cash (credit).
- If a column is a subtotal of other columns (e.g. total earnings = base + allowances), set role "ignore" so it is not double counted.
- Other roles: employee_name, employee_id, department, pay_date, ignore.
- Use only the provided accounts, entities and funds. If unsure, give a low confidence and explain in rationale.
- confidence is 0-1. rationale is one short sentence. memo is a short journal line description (may be empty).
Return JSON only, matching the schema."""


@dataclass
class Suggestion:
    lines: list[MappingLine]
    source: str                      # "claude" | "mock"
    model: str
    notice: str
    values_redacted: int = 0
    columns_redacted: list[str] = field(default_factory=list)
    payload_preview: dict | None = None


def response_schema(client: ClientConfig) -> dict:
    accounts = [""] + sorted(client.accounts)
    entities = [""] + client.entity_codes
    funds = [""] + sorted(client.funds)
    item = {
        "type": "object",
        "properties": {
            "source_column": {"type": "string"},
            "role": {"type": "string", "enum": list(ROLES)},
            "line_type": {"type": "string", "enum": [""] + list(LINE_TYPES)},
            "side": {"type": "string", "enum": [""] + list(SIDES)},
            "gl_account": {"type": "string", "enum": accounts},
            "offset_account": {"type": "string", "enum": accounts},
            "entity": {"type": "string", "enum": entities},
            "fund": {"type": "string", "enum": funds},
            "memo": {"type": "string"},
            "confidence": {"type": "number"},
            "rationale": {"type": "string"},
        },
        "required": ["source_column", "role", "line_type", "side", "gl_account", "offset_account",
                     "entity", "fund", "memo", "confidence", "rationale"],
        "additionalProperties": False,
    }
    return {"type": "object", "properties": {"lines": {"type": "array", "items": item}},
            "required": ["lines"], "additionalProperties": False}


def _user_message(redacted: RedactionResult, client: ClientConfig) -> str:
    context = {
        "report": redacted.payload,
        "chart_of_accounts": [{"account_no": a.account_no, "name": a.name, "category": a.category}
                              for a in client.accounts.values()],
        "entities": [{"code": e.code, "name": e.name, "is_paying_entity": e.is_paying} for e in client.entities],
        "funds": [{"code": c, "name": n} for c, n in client.funds.items()],
    }
    return json.dumps(context, indent=1)


def _clip(value: Any, n: int = 240) -> str:
    return str(value or "")[:n]


def normalize_ai_lines(raw_lines: list[dict], report: ParsedReport, client: ClientConfig,
                       token_map: dict[str, str], origin: str) -> list[MappingLine]:
    """Validate model output against the client's real chart; anything invalid is cleared, never trusted."""
    by_col = {normalize_header(str(r.get("source_column", ""))): r for r in raw_lines if isinstance(r, dict)}
    def_entity, def_fund = default_dimensions(client)
    lines: list[MappingLine] = []
    for header in report.headers:
        raw = by_col.get(normalize_header(header))
        if raw is None:
            lines.append(MappingLine(header, origin=origin, rationale="The suggestion did not cover this column."))
            continue
        role = raw.get("role") if raw.get("role") in ROLES else ""
        notes = [restore(_clip(raw.get("rationale")), token_map)]
        line = MappingLine(header, role, origin=origin, memo=restore(_clip(raw.get("memo"), 80), token_map))
        try:
            line.confidence = max(0.0, min(1.0, float(raw.get("confidence"))))
        except (TypeError, ValueError):
            line.confidence = None
        if role == "amount":
            line.line_type = raw.get("line_type") if raw.get("line_type") in LINE_TYPES else ""
            line.side = raw.get("side") if raw.get("side") in SIDES else ""
            for attr in ("gl_account", "offset_account"):
                value = str(raw.get(attr) or "")
                if value and value not in client.accounts:
                    notes.append(f"(suggested {attr.replace('_', ' ')} {value!r} is not in the chart and was cleared)")
                    value = ""
                setattr(line, attr, value)
            ent = str(raw.get("entity") or "")
            fnd = str(raw.get("fund") or "")
            if line.gl_account:
                line.line_type = client.line_type_for(line.gl_account)   # type follows the account, not the model
            line.entity = ent if client.entity(ent) else def_entity
            line.fund = fnd if fnd in client.funds else def_fund
            if not report.is_amount_column(header):
                line.role, line.line_type, line.side, line.gl_account, line.offset_account = "", "", "", "", ""
                notes.append("(this column does not contain amounts, so the role was cleared)")
        line.rationale = " ".join(n for n in notes if n)
        lines.append(line)
    return lines


def _call_claude(client_obj: Any, model: str, redacted: RedactionResult, client: ClientConfig) -> list[dict]:
    response = client_obj.messages.create(
        model=model,
        max_tokens=8000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": _user_message(redacted, client)}],
        output_config={"format": {"type": "json_schema", "schema": response_schema(client)}},
    )
    if getattr(response, "stop_reason", None) == "refusal":
        raise RuntimeError("the model declined the request")
    if getattr(response, "stop_reason", None) == "max_tokens":
        raise RuntimeError("the response was cut off")
    text = next((b.text for b in response.content if getattr(b, "type", "") == "text"), "")
    data = json.loads(text)
    return list(data["lines"])


def suggest_mapping(
    report: ParsedReport,
    client: ClientConfig,
    *,
    api_key: str | None = None,
    model: str | None = None,
    anthropic_client: Any = None,
) -> Suggestion:
    """Propose (never apply) a mapping for `report`. See module docstring for the privacy guarantees."""
    key = api_key if api_key is not None else os.environ.get("ANTHROPIC_API_KEY", "")
    redacted = build_model_payload(report)
    info = dict(values_redacted=redacted.values_redacted, columns_redacted=redacted.columns_redacted,
                payload_preview=redacted.payload)

    if not key and anthropic_client is None:
        return Suggestion(mock_lines(report, client), "mock", "mock-heuristic", MOCK_LABEL, **info)

    model = model or os.environ.get("ANTHROPIC_MODEL") or DEFAULT_MODEL
    try:
        if anthropic_client is None:
            import anthropic  # imported lazily so the demo runs without the SDK being touched

            anthropic_client = anthropic.Anthropic(api_key=key, timeout=90.0)
        raw = _call_claude(anthropic_client, model, redacted, client)
        lines = normalize_ai_lines(raw, report, client, redacted.token_map, "ai")
        notice = (f"AI SUGGESTION from {model}. Only redacted headers and {min(report.row_count, 3)} redacted sample rows were sent. "
                  "Review every line - nothing is applied until a Reviewer approves it.")
        return Suggestion(lines, "claude", model, notice, **info)
    except Exception as exc:  # network, auth, refusal, bad JSON ... never surface details of the payload
        notice = (f"{MOCK_LABEL.replace('ANTHROPIC_API_KEY is not set', 'the AI call failed: ' + type(exc).__name__)}")
        return Suggestion(mock_lines(report, client), "mock", "mock-heuristic", notice, **info)


# --------------------------------------------------------------------------------------------
# Offline mock: looser keyword matching than rules.py, plus a subtotal detector. NOT an AI model.
# --------------------------------------------------------------------------------------------
def _has(norm: str, *words: str) -> bool:
    return any(re.search(rf"\b{w}\b", norm) for w in words)


def _find_subtotals(report: ParsedReport) -> dict[str, list[str]]:
    """Columns whose every row equals the sum of two or more other amount columns."""
    if report.row_count < 3:
        return {}   # too few rows for "every row adds up" to mean anything
    cols = report.amount_columns()
    series = {c: report.amounts(c) for c in cols}
    out: dict[str, list[str]] = {}
    for target in cols:
        t = series[target]
        if not t or not any(t):
            continue
        # all-zero columns are excluded: x + 0 == x would make every column look like a subtotal
        others = [c for c in cols if c != target and len(series[c]) == len(t) and any(series[c])]
        for i, a in enumerate(others):
            for b in others[i + 1:]:
                if all(x + y == z for x, y, z in zip(series[a], series[b], t)):
                    out[target] = [a, b]
    return out


def mock_lines(report: ParsedReport, client: ClientConfig) -> list[MappingLine]:
    def_entity, def_fund = default_dimensions(client)
    subtotals = _find_subtotals(report)
    lines: list[MappingLine] = []

    def amount(header: str, line_type: str, side: str, category: str, offset: str, memo: str,
               conf: float, why: str) -> MappingLine:
        return MappingLine(
            header, "amount", line_type, side, client.account_for_category(category), def_entity, def_fund,
            client.account_for_category(offset) if offset else "", memo, origin="mock", confidence=conf,
            rationale="MOCK: " + why)

    for h in report.headers:
        n = normalize_header(h)
        employer = _has(n, "er", "employer", "org", "organization", "organisation", "company")
        if not report.is_amount_column(h):
            if _has(n, "name", "payee"):
                lines.append(MappingLine(h, "employee_name", origin="mock", confidence=0.8, rationale="MOCK: header contains 'name'"))
            elif _has(n, "date"):
                lines.append(MappingLine(h, "pay_date", origin="mock", confidence=0.7, rationale="MOCK: header contains 'date'"))
            elif _has(n, "id", "number", "no", "ssn") or n.endswith(" id"):
                lines.append(MappingLine(h, "employee_id", origin="mock", confidence=0.7, rationale="MOCK: header looks like an ID"))
            elif _has(n, "dept", "department", "centre", "center", "division"):
                lines.append(MappingLine(h, "department", origin="mock", confidence=0.7, rationale="MOCK: header looks like a department"))
            else:
                lines.append(MappingLine(h, origin="mock", rationale="MOCK: no keyword matched - assign a role yourself"))
            continue
        if h in subtotals:
            a, b = subtotals[h]
            lines.append(MappingLine(h, "ignore", origin="mock", confidence=0.85,
                                     rationale=f"MOCK: every row equals '{a}' + '{b}', so this looks like a subtotal; posting it would double count"))
        elif _has(n, "disbursed", "net", "take", "home") and not employer:
            lines.append(amount(h, "cash", "credit", "cash", "", "Net pay disbursed", 0.8, "header says net/disbursed amount -> cash"))
        elif _has(n, "soc", "social", "medicare", "fica", "ss") and employer:
            lines.append(amount(h, "expense", "debit", "payroll_tax_expense", "fica_payable", "Employer payroll taxes", 0.7, "employer-side social security/Medicare -> expense with FICA payable offset"))
        elif _has(n, "soc", "social", "medicare", "fica", "ss"):
            lines.append(amount(h, "liability", "credit", "fica_payable", "", "Employee FICA withheld", 0.7, "employee-side social security/Medicare -> FICA payable"))
        elif _has(n, "medical", "health", "dental", "insurance") and employer:
            lines.append(amount(h, "expense", "debit", "benefits_expense", "health_payable", "Employer health benefits", 0.7, "employer-side medical -> benefits expense with payable offset"))
        elif _has(n, "medical", "health", "dental", "insurance"):
            lines.append(amount(h, "liability", "credit", "health_payable", "", "Employee health deduction", 0.7, "employee-side medical -> health payable"))
        elif _has(n, "annuity", "403", "401", "retirement", "pension", "tsa") and employer:
            lines.append(amount(h, "expense", "debit", "retirement_expense", "retirement_payable", "Employer retirement match", 0.6, "employer-side annuity/retirement -> expense with payable offset"))
        elif _has(n, "annuity", "403", "401", "retirement", "pension", "tsa"):
            lines.append(amount(h, "liability", "credit", "retirement_payable", "", "Employee retirement deduction", 0.6, "employee-side annuity/retirement -> retirement payable"))
        elif _has(n, "fed", "federal") or ("statutory" in n and _has(n, "fed", "federal")):
            lines.append(amount(h, "liability", "credit", "fed_wh_payable", "", "Federal income tax withheld", 0.75, "federal tax withheld -> payable"))
        elif _has(n, "state"):
            lines.append(amount(h, "liability", "credit", "state_wh_payable", "", "State income tax withheld", 0.75, "state tax withheld -> payable"))
        elif _has(n, "housing", "allowance", "parsonage"):
            housing = client.account_for_category("housing_expense") or client.account_for_category("salary_expense")
            line = amount(h, "expense", "debit", "housing_expense" if client.account_for_category("housing_expense") else "salary_expense",
                          "", "Clergy housing allowance", 0.55, "allowance is compensation -> wages/housing expense (confirm the account)")
            line.gl_account = housing
            lines.append(line)
        elif _has(n, "comp", "compensation", "earnings", "wages", "salary", "pay", "gross", "base"):
            lines.append(amount(h, "expense", "debit", "salary_expense", "", "Gross wages", 0.65, "compensation/earnings -> salaries expense"))
        else:
            lines.append(MappingLine(h, origin="mock", rationale="MOCK: amount column, but no keyword matched - assign it yourself"))
    return lines
