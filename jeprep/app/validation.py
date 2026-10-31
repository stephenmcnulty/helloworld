"""Pre-export checks. Export is blocked unless none of them has status 'fail'."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Sequence

from .domain import ClientConfig, MappingLine
from .journal import DraftJournal
from .money import ZERO, fmt_money, parse_date
from .parsing import ParsedReport

PASS, FAIL, WARN = "pass", "fail", "warn"


@dataclass
class CheckResult:
    id: str
    label: str
    status: str
    detail: str

    @property
    def passed(self) -> bool:
        return self.status != FAIL


@dataclass
class TieOutRow:
    column: str
    source_total: Decimal
    stated_total: Decimal | None
    journal_amount: Decimal
    note: str = ""

    @property
    def vs_stated(self) -> Decimal | None:
        return None if self.stated_total is None else self.source_total - self.stated_total

    @property
    def vs_journal(self) -> Decimal:
        return self.source_total - self.journal_amount


def tie_out(report: ParsedReport, mapping: Sequence[MappingLine], journal: DraftJournal) -> list[TieOutRow]:
    """For every amount column: report total vs the report's own totals row vs what the journal carries."""
    in_journal: dict[str, Decimal] = {}
    for l in journal.lines:
        if l.kind != "source":
            continue
        mapped_side_amount = (l.debit - l.credit)
        # Re-express on the mapped side: the sign flag records negative totals that were flipped.
        in_journal[l.source_column] = in_journal.get(l.source_column, ZERO) + abs(mapped_side_amount) * l.sign
    rows: list[TieOutRow] = []
    seen: set[str] = set()
    for ml in mapping:
        if ml.role not in ("amount", "ignore") or ml.source_column in seen or ml.source_column not in report.headers:
            continue
        if ml.role == "ignore" and not report.is_amount_column(ml.source_column):
            continue
        seen.add(ml.source_column)
        rows.append(TieOutRow(
            ml.source_column,
            report.column_total(ml.source_column),
            report.stated_total(ml.source_column),
            in_journal.get(ml.source_column, ZERO),
            "ignored - not posted" if ml.role == "ignore" else "",
        ))
    return rows


def check_mapping_complete(report: ParsedReport, mapping: Sequence[MappingLine], client: ClientConfig) -> CheckResult:
    label = "No unmapped lines"
    by_col = {m.source_column: m for m in mapping}
    problems: list[str] = []
    for header in report.headers:
        ml = by_col.get(header)
        if ml is None:
            problems.append(f"'{header}': column is not in the approved mapping")
            continue
        for p in ml.problems(client):
            problems.append(f"'{header}': {p}")
    amount_cols = [m for m in mapping if m.role == "amount"]
    if not amount_cols and not problems:
        problems.append("no report column is mapped to a journal line")
    if problems:
        shown = "; ".join(problems[:4]) + (f"; and {len(problems) - 4} more" if len(problems) > 4 else "")
        return CheckResult("mapping_complete", label, FAIL, shown)
    return CheckResult("mapping_complete", label, PASS,
                       f"All {len(report.headers)} report columns have a role; every posting line has a valid account, entity and fund.")


def check_balanced(journal: DraftJournal) -> CheckResult:
    label = "Debits equal credits"
    d, c = journal.total_debits, journal.total_credits
    if len(journal.lines) < 2 or d == ZERO:
        return CheckResult("balanced", label, FAIL, "The journal has no postable lines.")
    if d != c:
        return CheckResult("balanced", label, FAIL,
                           f"Debits {fmt_money(d)} vs credits {fmt_money(c)} - out of balance by {fmt_money(abs(d - c))}. "
                           "The source report may not foot (gross - deductions != net) or a column is mapped to the wrong side.")
    return CheckResult("balanced", label, PASS, f"Debits and credits both total {fmt_money(d)}.")


def check_entities_balanced(journal: DraftJournal) -> CheckResult:
    label = "Each entity balances on its own"
    bad = [(e, d, c) for e, (d, c) in journal.by_entity().items() if d != c]
    if bad:
        parts = [f"{e} is out by {fmt_money(abs(d - c))} (Dr {fmt_money(d)} / Cr {fmt_money(c)})" for e, d, c in bad]
        return CheckResult("entities_balanced", label, FAIL,
                           "; ".join(parts) + ". Turn on allocation or map every line to one entity.")
    return CheckResult("entities_balanced", label, PASS,
                       f"{len(journal.by_entity())} entit{'y' if len(journal.by_entity()) == 1 else 'ies'} checked.")


def check_totals_tie(rows: Sequence[TieOutRow]) -> CheckResult:
    label = "Totals tie back to the source report"
    problems: list[str] = []
    for r in rows:
        if r.vs_stated not in (None, ZERO):
            problems.append(f"'{r.column}': rows add to {fmt_money(r.source_total)} but the report's own total row says {fmt_money(r.stated_total)}")
        if r.note == "" and r.vs_journal != ZERO:
            problems.append(f"'{r.column}': report {fmt_money(r.source_total)} vs journal {fmt_money(r.journal_amount)}")
    if problems:
        shown = "; ".join(problems[:3]) + (f"; and {len(problems) - 3} more" if len(problems) > 3 else "")
        return CheckResult("totals_tie", label, FAIL, shown)
    ignored = [r for r in rows if r.note and r.source_total != ZERO]
    stated = sum(1 for r in rows if r.stated_total is not None)
    detail = f"{len([r for r in rows if not r.note])} posted columns match the journal"
    detail += f"; {stated} agree with the report's total row." if stated else "; the report has no total row to compare against."
    if ignored:
        return CheckResult("totals_tie", label, WARN,
                           detail + " Ignored columns with non-zero totals: " + ", ".join(r.column for r in ignored) + ".")
    return CheckResult("totals_tie", label, PASS, detail)


def check_dates(report: ParsedReport, mapping: Sequence[MappingLine], journal: DraftJournal,
                period_start: date, period_end: date) -> CheckResult:
    label = "Dates fall within the selected pay period"
    if period_start > period_end:
        return CheckResult("dates", label, FAIL, "The period start date is after the period end date.")
    if not (period_start <= journal.posting_date <= period_end):
        return CheckResult("dates", label, FAIL, f"Journal date {journal.posting_date:%m/%d/%Y} is outside the period.")
    date_cols = [m.source_column for m in mapping if m.role == "pay_date" and m.source_column in report.headers]
    if not date_cols:
        return CheckResult("dates", label, WARN,
                           f"Journal date {journal.posting_date:%m/%d/%Y} is inside the period, but no pay-date column is mapped, "
                           "so dates in the report could not be checked.")
    unparsable, outside = 0, []
    for value in report.values(date_cols[0]):
        if not value.strip():
            continue
        d = parse_date(value)
        if d is None:
            unparsable += 1
        elif not (period_start <= d <= period_end):
            outside.append(d)
    if unparsable or outside:
        bits = []
        if outside:
            sample = ", ".join(sorted({f"{d:%m/%d/%Y}" for d in outside})[:3])
            bits.append(f"{len(outside)} row(s) dated outside {period_start:%m/%d/%Y}-{period_end:%m/%d/%Y} (e.g. {sample})")
        if unparsable:
            bits.append(f"{unparsable} row(s) with an unreadable date")
        return CheckResult("dates", label, FAIL, "; ".join(bits) + ".")
    return CheckResult("dates", label, PASS,
                       f"All {report.row_count} pay dates and the journal date are within {period_start:%m/%d/%Y}-{period_end:%m/%d/%Y}.")


def run_checks(
    report: ParsedReport,
    mapping: Sequence[MappingLine],
    client: ClientConfig,
    journal: DraftJournal,
    period_start: date,
    period_end: date,
) -> tuple[list[CheckResult], list[TieOutRow]]:
    rows = tie_out(report, mapping, journal)
    checks = [
        check_mapping_complete(report, mapping, client),
        check_balanced(journal),
        check_entities_balanced(journal),
        check_totals_tie(rows),
        check_dates(report, mapping, journal, period_start, period_end),
    ]
    return checks, rows


def all_passed(checks: Sequence[CheckResult]) -> bool:
    return all(c.status != FAIL for c in checks)
