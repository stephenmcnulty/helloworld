"""Write the import-ready CSV for the chosen target system. Nothing here talks to a network.

IMPORTANT - these column layouts follow the vendors' *standard* journal-entry import templates as
best understood when this demo was written, without access to a live tenant. Every tenant can add
dimensions (and Intacct/QBO change templates over time), so before production use, diff each layout
against a template downloaded from the client's own Intacct / QBO company. Assumptions to confirm:
  * Intacct: entity -> LOCATION_ID, fund -> CLASSID (many nonprofits use a custom FUND dimension).
  * QBO:     entity -> Location, fund -> Class, account matched by "<number> <name>" (account numbers on).
"""
from __future__ import annotations

import csv
import io
import re
from dataclasses import dataclass
from decimal import Decimal

from .domain import TARGET_SYSTEMS
from .journal import DraftJournal, JournalLine
from .money import ZERO, fmt_date_us, q

INTACCT_COLUMNS = [
    "DONOTIMPORT", "JOURNAL", "DATE", "REVERSEDATE", "DESCRIPTION", "REFERENCE_NO", "LINE_NO",
    "ACCT_NO", "LOCATION_ID", "DEPT_ID", "CLASSID", "DOCUMENT", "MEMO", "DEBIT", "CREDIT",
    "SOURCEENTITY", "CURRENCY", "STATE",
]
INTACCT_JOURNAL_SYMBOL = "GJ"   # General journal symbol; confirm the symbol the client's company uses.

QBO_COLUMNS = [
    "JournalNo", "JournalDate", "Currency", "Memo", "Account", "Debits", "Credits",
    "Description", "Name", "Location", "Class",
]
QBO_ACCOUNT_FORMAT = "{number} {name}"

_CONTROL_RE = re.compile(r"[\x00-\x1f\x7f]+")


class ExportBlocked(RuntimeError):
    pass


def safe_text(value: str) -> str:
    """Neutralise spreadsheet formula injection and strip control characters from a text cell."""
    cleaned = _CONTROL_RE.sub(" ", str(value)).strip()
    if cleaned and cleaned[0] in "=+-@":
        cleaned = "'" + cleaned
    return cleaned


def _amount(value: Decimal) -> str:
    return "" if value == ZERO else f"{q(value):.2f}"


def intacct_rows(j: DraftJournal) -> list[list[str]]:
    date = fmt_date_us(j.posting_date)
    rows = []
    for l in j.lines:
        rows.append([
            "", INTACCT_JOURNAL_SYMBOL, date, "", safe_text(j.description), safe_text(j.reference),
            str(l.line_no), l.account_no, l.entity, "", l.fund, safe_text(j.reference),
            safe_text(l.memo), _amount(l.debit), _amount(l.credit), "", "USD", "Posted",
        ])
    return rows


def qbo_rows(j: DraftJournal) -> list[list[str]]:
    date = fmt_date_us(j.posting_date)
    rows = []
    for l in j.lines:
        account = QBO_ACCOUNT_FORMAT.format(number=l.account_no, name=l.account_name)
        rows.append([
            safe_text(j.reference), date, "USD", safe_text(j.description), safe_text(account),
            _amount(l.debit), _amount(l.credit), safe_text(l.memo), "", l.entity, l.fund,
        ])
    return rows


@dataclass(frozen=True)
class ExportFile:
    filename: str
    content: bytes
    row_count: int
    columns: list[str]


def export_journal(j: DraftJournal) -> ExportFile:
    if j.target not in TARGET_SYSTEMS:
        raise ValueError(f"Unknown target system {j.target!r}")
    if j.total_debits != j.total_credits or not j.lines:
        raise ExportBlocked("Refusing to write an unbalanced journal.")
    columns, rows = (INTACCT_COLUMNS, intacct_rows(j)) if j.target == "intacct" else (QBO_COLUMNS, qbo_rows(j))
    buf = io.StringIO()
    writer = csv.writer(buf, lineterminator="\r\n")
    writer.writerow(columns)
    writer.writerows(rows)
    slug = re.sub(r"[^A-Za-z0-9]+", "-", j.client_name).strip("-").lower()
    name = f"JE_{slug}_{j.posting_date:%Y%m%d}_{j.target}.csv"
    return ExportFile(name, buf.getvalue().encode("utf-8"), len(rows), columns)
