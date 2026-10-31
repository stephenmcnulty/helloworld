"""Money and date helpers. All amounts are Decimal; floats never touch a posting amount."""
from __future__ import annotations

import re
from datetime import date, datetime
from decimal import ROUND_HALF_UP, Decimal

CENT = Decimal("0.01")
ZERO = Decimal("0.00")

_MONEY_RE = re.compile(r"^[+-]?(\d+(\.\d*)?|\.\d+)$")
_DATE_FORMATS = ("%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y", "%Y/%m/%d", "%d-%b-%Y", "%b %d, %Y", "%B %d, %Y", "%m-%d-%Y")
_ISO_DATETIME_RE = re.compile(r"^\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}")


def q(value: Decimal) -> Decimal:
    """Round to cents (half-up, the usual accounting convention)."""
    return value.quantize(CENT, rounding=ROUND_HALF_UP)


def parse_money(raw: object) -> Decimal | None:
    """Parse '$1,234.50', '(12.00)', '-5', '12-' into a cents-quantized Decimal; None if not money."""
    if raw is None:
        return None
    text = str(raw).strip()
    if not text or len(text) > 24:
        return None
    negative = False
    if text.startswith("(") and text.endswith(")"):
        negative, text = True, text[1:-1]
    text = text.replace("$", "").replace(",", "").replace(" ", "")
    if text.endswith("-"):
        negative, text = True, text[:-1]
    if not _MONEY_RE.match(text):
        return None
    value = Decimal(text)
    return q(-value if negative else value)


def parse_date(raw: object) -> date | None:
    text = str(raw).strip() if raw is not None else ""
    if not text:
        return None
    if _ISO_DATETIME_RE.match(text):
        text = text[:10]
    for fmt in _DATE_FORMATS:
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            continue
    return None


def fmt_money(value: Decimal) -> str:
    return f"{value:,.2f}"


def fmt_date_us(value: date) -> str:
    return value.strftime("%m/%d/%Y")
