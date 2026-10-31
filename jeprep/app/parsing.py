"""Turn an uploaded CSV/XLSX payroll register into a typed, in-memory report.

Cells are read as strings and converted to Decimal only when summed, so no float ever touches money.
The file is never executed or evaluated: Excel formulas are read as cached values only.
"""
from __future__ import annotations

import csv
import hashlib
import io
import math
import re
from dataclasses import dataclass, field
from decimal import Decimal

import pandas as pd

from .money import ZERO, parse_money

TOTAL_ROW_RE = re.compile(r"^\s*(grand\s+)?totals?\s*:?\s*$", re.I)
SUBTOTAL_ROW_RE = re.compile(r"^\s*sub\s*-?\s*totals?\b", re.I)


class ParseError(ValueError):
    """The file is readable but isn't a usable report; the message is safe to show to the user."""


def normalize_header(header: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", header.lower()).strip()


def layout_signature(headers: list[str]) -> str:
    """Order-insensitive fingerprint of the column set; identical layouts share a signature."""
    joined = "|".join(sorted(normalize_header(h) for h in headers))
    return hashlib.sha256(joined.encode("utf-8")).hexdigest()


@dataclass
class ParsedReport:
    headers: list[str]
    df: pd.DataFrame                    # data rows only, every cell a str
    totals_row: dict[str, str] | None = None
    title_lines: list[str] = field(default_factory=list)
    skipped_rows: int = 0               # blank rows and subtotal rows ignored

    @property
    def layout_signature(self) -> str:
        return layout_signature(self.headers)

    @property
    def row_count(self) -> int:
        return len(self.df)

    def values(self, column: str) -> list[str]:
        return [str(v) for v in self.df[column].tolist()]

    def amounts(self, column: str) -> list[Decimal]:
        return [m for m in (parse_money(v) for v in self.values(column)) if m is not None]

    def column_total(self, column: str) -> Decimal:
        return sum(self.amounts(column), ZERO)

    def stated_total(self, column: str) -> Decimal | None:
        if not self.totals_row:
            return None
        return parse_money(self.totals_row.get(column, ""))

    def is_amount_column(self, column: str) -> bool:
        non_empty = [v for v in self.values(column) if v.strip()]
        return bool(non_empty) and all(parse_money(v) is not None for v in non_empty)

    def amount_columns(self) -> list[str]:
        return [h for h in self.headers if self.is_amount_column(h)]


def _decode_csv(data: bytes) -> str:
    for encoding in ("utf-8-sig", "cp1252"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    raise ParseError("The CSV could not be decoded. Save it as UTF-8 and upload again.")


def _csv_grid(data: bytes, max_rows: int) -> list[list[str]]:
    text = _decode_csv(data)
    sample = text[:4096]
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=",;\t|")
        delimiter = dialect.delimiter
    except csv.Error:
        delimiter = ","
    grid: list[list[str]] = []
    for row in csv.reader(io.StringIO(text), delimiter=delimiter):
        grid.append([c.strip() for c in row])
        if len(grid) > max_rows + 50:
            raise ParseError(f"The report has more than {max_rows:,} rows, which is over the limit.")
    return grid


def _xlsx_grid(data: bytes, max_rows: int) -> list[list[str]]:
    try:
        frame = pd.read_excel(io.BytesIO(data), header=None, dtype=str, engine="openpyxl", sheet_name=0)
    except Exception as exc:  # openpyxl/zip raise many types; never echo file contents back
        raise ParseError("The Excel file could not be read. Is it a valid .xlsx workbook?") from exc
    if len(frame) > max_rows + 50:
        raise ParseError(f"The report has more than {max_rows:,} rows, which is over the limit.")
    grid: list[list[str]] = []
    for row in frame.itertuples(index=False):
        grid.append(["" if pd.isna(v) else str(v).strip() for v in row])
    return grid


def _find_header_row(grid: list[list[str]]) -> int:
    scan = grid[:15]
    counts = [sum(1 for c in row if c) for row in scan]
    widest = max(counts, default=0)
    if widest < 2:
        raise ParseError("No table was found in the file (need at least two columns).")
    needed = max(2, math.ceil(0.6 * widest))
    for i, row in enumerate(scan):
        cells = [c for c in row if c]
        if len(cells) >= needed:
            textual = sum(1 for c in cells if parse_money(c) is None)
            if textual / len(cells) >= 0.8:
                return i
    raise ParseError("Could not find a header row in the first 15 rows of the file.")


def _clean_headers(raw: list[str]) -> list[str]:
    headers, seen = [], {}
    for i, h in enumerate(raw, start=1):
        name = re.sub(r"\s+", " ", h).strip() or f"Column {i}"
        count = seen.get(name.lower(), 0) + 1
        seen[name.lower()] = count
        headers.append(name if count == 1 else f"{name} ({count})")
    return headers


def parse_report(data: bytes, ext: str, *, max_rows: int = 20000, max_columns: int = 100) -> ParsedReport:
    grid = _xlsx_grid(data, max_rows) if ext == ".xlsx" else _csv_grid(data, max_rows)
    width = max((len(r) for r in grid), default=0)
    grid = [r + [""] * (width - len(r)) for r in grid]
    header_idx = _find_header_row(grid)
    title_lines = [" ".join(c for c in row if c) for row in grid[:header_idx] if any(row)]
    headers = _clean_headers(grid[header_idx])

    body = grid[header_idx + 1:]
    # Drop columns with no header and no data (trailing empty columns are common in exports).
    keep = [i for i in range(width) if grid[header_idx][i] or any(r[i] for r in body)]
    if len(keep) > max_columns:
        raise ParseError(f"The report has more than {max_columns} columns, which is over the limit.")
    headers = [headers[i] for i in keep]

    rows: list[list[str]] = []
    totals: dict[str, str] | None = None
    skipped = 0
    for raw in body:
        row = [raw[i] for i in keep]
        if not any(row):
            skipped += 1
            continue
        label_cells = [c for c in row[:2] if c]
        label = label_cells[0] if label_cells else ""
        if SUBTOTAL_ROW_RE.match(label):
            skipped += 1
        elif TOTAL_ROW_RE.match(label):
            totals = dict(zip(headers, row))
        else:
            rows.append(row)
    if not rows:
        raise ParseError("The report has a header but no data rows.")
    df = pd.DataFrame(rows, columns=headers, dtype=object)
    return ParsedReport(headers=headers, df=df, totals_row=totals, title_lines=title_lines, skipped_rows=skipped)
