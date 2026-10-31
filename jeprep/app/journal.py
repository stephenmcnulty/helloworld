"""Build the draft journal entry from a parsed report + an approved mapping (+ optional allocation)."""
from __future__ import annotations

import hashlib
import json
from collections import OrderedDict
from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from typing import Sequence

from .allocation import interco_lines, split_amount
from .domain import ClientConfig, MappingLine
from .money import ZERO
from .parsing import ParsedReport


@dataclass
class JournalLine:
    line_no: int
    account_no: str
    account_name: str
    entity: str
    fund: str
    debit: Decimal
    credit: Decimal
    memo: str
    kind: str                  # "source" (a report column), "offset", or "interco"
    source_column: str = ""
    sign: int = 1              # +1 when posted on the mapped side, -1 when a negative total flipped it


@dataclass
class DraftJournal:
    reference: str
    posting_date: date
    description: str
    target: str
    client_name: str
    lines: list[JournalLine] = field(default_factory=list)
    zero_columns: list[str] = field(default_factory=list)   # mapped columns whose total is 0 (no line made)

    @property
    def total_debits(self) -> Decimal:
        return sum((l.debit for l in self.lines), ZERO)

    @property
    def total_credits(self) -> Decimal:
        return sum((l.credit for l in self.lines), ZERO)

    def by_entity(self) -> "OrderedDict[str, tuple[Decimal, Decimal]]":
        out: "OrderedDict[str, list[Decimal]]" = OrderedDict()
        for l in self.lines:
            d = out.setdefault(l.entity, [ZERO, ZERO])
            d[0] += l.debit
            d[1] += l.credit
        return OrderedDict((k, (v[0], v[1])) for k, v in out.items())

    def content_hash(self) -> str:
        """Stable fingerprint of exactly what would be exported; approvals are bound to it."""
        payload = {
            "ref": self.reference, "date": self.posting_date.isoformat(), "desc": self.description,
            "target": self.target,
            "lines": [[l.account_no, l.entity, l.fund, str(l.debit), str(l.credit), l.memo] for l in self.lines],
        }
        blob = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def _flip(side: str) -> str:
    return "credit" if side == "debit" else "debit"


def build_journal(
    report: ParsedReport,
    mapping: Sequence[MappingLine],
    client: ClientConfig,
    *,
    period_start: date,
    period_end: date,
    allocate: bool,
    target: str,
    report_label: str = "Payroll register",
) -> DraftJournal:
    """Aggregate each mapped amount column into a journal line.

    Incomplete mapping lines are skipped here (and reported by the validation checks) so a partial
    mapping still produces a previewable, but un-exportable, journal.
    """
    journal = DraftJournal(
        reference=f"PR-{client.id.upper()}-{period_end:%Y%m%d}"[:40],
        posting_date=period_end,
        description=f"{report_label} {period_start:%m/%d/%Y}-{period_end:%m/%d/%Y} - {client.name}",
        target=target,
        client_name=client.name,
    )
    drafts: list[tuple[MappingLine, JournalLine]] = []
    for ml in mapping:
        if not ml.is_postable(client):
            continue
        total = report.column_total(ml.source_column)
        if total == ZERO:
            journal.zero_columns.append(ml.source_column)
            continue
        amount, sign = abs(total), (1 if total > 0 else -1)
        side = ml.side if sign == 1 else _flip(ml.side)
        label = ml.memo or ml.source_column

        def make(account: str, side_: str, kind: str, memo: str) -> JournalLine:
            return JournalLine(
                0, account, client.accounts[account].name, ml.entity, ml.fund,
                amount if side_ == "debit" else ZERO, amount if side_ == "credit" else ZERO,
                memo, kind, ml.source_column, sign,
            )

        drafts.append((ml, make(ml.gl_account, side, "source", label)))
        if ml.offset_account:
            drafts.append((ml, make(ml.offset_account, _flip(side), "offset", f"{label} - offset")))

    lines: list[JournalLine] = []
    for ml, line in drafts:
        if allocate and line.kind == "source" and ml.line_type == "expense":
            weights = [(e.code, e.alloc_pct) for e in client.entities]
            parts = split_amount(line.debit - line.credit, weights)
            pct = {e.code: e.alloc_pct for e in client.entities}
            for ent in client.entities:
                share = parts[ent.code]
                if share == ZERO:
                    continue
                fund = ent.default_fund if ent.default_fund in client.funds else line.fund
                lines.append(JournalLine(
                    0, line.account_no, line.account_name, ent.code, fund,
                    share if share > 0 else ZERO, -share if share < 0 else ZERO,
                    f"{line.memo} - {pct[ent.code].normalize():f}% {ent.code}", "source",
                    line.source_column, line.sign,
                ))
        else:
            lines.append(line)

    if allocate and not client.allocation_problems():
        payer = client.paying_entity
        net: "OrderedDict[str, Decimal]" = OrderedDict((e.code, ZERO) for e in client.entities)
        for l in lines:
            net[l.entity] = net.get(l.entity, ZERO) + l.debit - l.credit
        for ic in interco_lines(net, payer.code, client.due_from_account, client.due_to_account):
            lines.append(JournalLine(
                0, ic.account_no, client.accounts[ic.account_no].name, ic.entity,
                client.default_fund_for(ic.entity), ic.debit, ic.credit, ic.memo, "interco",
            ))

    for i, l in enumerate(lines, start=1):
        l.line_no = i
    journal.lines = lines
    return journal
