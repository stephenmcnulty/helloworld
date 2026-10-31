"""Redact employee identifiers *before* anything is sent to a model.

What leaves the building: column headers, the row count, and at most a few sample rows in which
every employee name / ID / other identifying text has been replaced by a token (EMP_001, ID_001 ...).
The token map exists only in memory for the duration of one suggestion request and is used to put
real values back into the model's text answer. Amounts and dates are sent as-is (they are needed
to work out what a column means); they are not linked to a person once the name/ID is tokenised.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from .parsing import ParsedReport
from .money import parse_date, parse_money

NAME_HEADER_RE = re.compile(r"(\bname\b|\bpayee\b)|^(employee|worker|staff|emp)$", re.I)
ID_HEADER_RE = re.compile(
    r"\b(ssn|tin|itin)\b|social security (no|number)|"
    r"((employee|emp|worker|staff|payee|person)\s*(id|number|no|num|#))|^(id|#)$|\bemp\s*#|\bworker\s*#", re.I)
SSN_RE = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
TOKEN_RE = re.compile(r"\b(?:EMP|ID|TXT|PII)_\d{3,}\b")

SAMPLE_ROWS = 3


@dataclass
class RedactionResult:
    payload: dict
    token_map: dict[str, str] = field(default_factory=dict)     # token -> real value (local only)
    columns_redacted: list[str] = field(default_factory=list)
    values_redacted: int = 0


class _Tokenizer:
    def __init__(self) -> None:
        self.by_value: dict[tuple[str, str], str] = {}
        self.token_map: dict[str, str] = {}
        self.counters: dict[str, int] = {}

    def token(self, prefix: str, value: str) -> str:
        key = (prefix, value.strip().lower())
        if key not in self.by_value:
            self.counters[prefix] = self.counters.get(prefix, 0) + 1
            tok = f"{prefix}_{self.counters[prefix]:03d}"
            self.by_value[key] = tok
            self.token_map[tok] = value.strip()
        return self.by_value[key]


def pii_columns(report: ParsedReport) -> dict[str, str]:
    """column -> token prefix. Header patterns first, then high-cardinality free text as a safety net."""
    found: dict[str, str] = {}
    for h in report.headers:
        if ID_HEADER_RE.search(h):
            found[h] = "ID"
        elif NAME_HEADER_RE.search(h) and not report.is_amount_column(h):
            found[h] = "EMP"
    n = report.row_count
    for h in report.headers:
        if h in found:
            continue
        if report.is_amount_column(h):
            # A column of same-length, mostly-unique whole numbers (1001, 1002 ...) is an ID, not money.
            vals = [v.strip() for v in report.values(h) if v.strip()]
            if (n >= 3 and all(re.fullmatch(r"\d{4,12}", v) for v in vals) and len({len(v) for v in vals}) == 1
                    and len(set(vals)) / len(vals) >= 0.9):
                found[h] = "ID"
            continue
        vals = [v for v in report.values(h) if v.strip()]
        if not vals or all(parse_date(v) for v in vals):
            continue
        if n >= 4 and len(set(v.lower() for v in vals)) / max(len(vals), 1) >= 0.8:
            found[h] = "TXT"   # looks like per-person text we don't recognise: redact it
    return found


def scrub(text: str, tk: _Tokenizer, known: dict[str, str]) -> tuple[str, int]:
    """Remove known identifiers, SSN-shaped numbers and emails from free text; returns (text, replacements)."""
    count = 0

    def sub_ssn(m: re.Match) -> str:
        nonlocal count
        count += 1
        return tk.token("PII", m.group(0))

    out = SSN_RE.sub(sub_ssn, text)
    out = EMAIL_RE.sub(sub_ssn, out)
    for value, tok in sorted(known.items(), key=lambda kv: -len(kv[0])):
        if len(value) >= 3:
            pattern = re.compile(re.escape(value), re.I)
            out, n = pattern.subn(tok, out)
            count += n
    return out, count


def build_model_payload(report: ParsedReport, sample_rows: int = SAMPLE_ROWS) -> RedactionResult:
    tk = _Tokenizer()
    pii = pii_columns(report)

    # Every distinct identifier in the *whole* file (not just the sample) so stray mentions are caught.
    known: dict[str, str] = {}
    for col, prefix in pii.items():
        for v in report.values(col):
            if v.strip():
                known[v.strip()] = tk.token(prefix, v)

    redacted = 0
    rows: list[dict[str, str]] = []
    for _, row in report.df.head(sample_rows).iterrows():
        out: dict[str, str] = {}
        for h in report.headers:
            value = str(row[h])
            if h in pii and value.strip():
                out[h] = tk.token(pii[h], value)
                redacted += 1
            elif report.is_amount_column(h) or parse_date(value) or parse_money(value) is not None:
                out[h] = value
            else:
                out[h], n = scrub(value, tk, known)
                redacted += n
        rows.append(out)

    headers = []
    for h in report.headers:
        clean, n = scrub(h, tk, known)
        headers.append(clean)
        redacted += n

    # Only tokens that actually appear in the outgoing payload need to be restorable.
    payload = {"columns": headers, "row_count": report.row_count, "sample_rows": rows}
    used = set(TOKEN_RE.findall(str(payload)))
    return RedactionResult(
        payload=payload,
        token_map={t: v for t, v in tk.token_map.items() if t in used},
        columns_redacted=sorted(pii),
        values_redacted=redacted,
    )


def restore(text: str, token_map: dict[str, str]) -> str:
    """Put real values back into text the model returned (e.g. a rationale that quoted a token)."""
    return TOKEN_RE.sub(lambda m: token_map.get(m.group(0), m.group(0)), text)
