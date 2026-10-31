"""Allocation math: percentage splits in whole cents, and the balancing inter-entity lines."""
from __future__ import annotations

from dataclasses import dataclass
from decimal import ROUND_FLOOR, Decimal
from typing import Mapping, Sequence

from .money import ZERO, q


class AllocationError(ValueError):
    pass


def split_amount(amount: Decimal, weights: Sequence[tuple[str, Decimal]]) -> dict[str, Decimal]:
    """Split `amount` across entities by percentage so the parts add up to exactly `amount`.

    Largest-remainder method on whole cents: each entity gets the floor of its exact share, then the
    leftover cents go to the largest fractional remainders (ties broken by configured order), so the
    result is deterministic and never loses or invents a cent.
    """
    if not weights:
        raise AllocationError("No allocation entities configured.")
    total_pct = sum((pct for _, pct in weights), Decimal("0"))
    if total_pct != Decimal("100"):
        raise AllocationError(f"Allocation percentages add up to {total_pct}%, not 100%.")
    cents_signed = int((q(amount) * 100).to_integral_value())
    sign = -1 if cents_signed < 0 else 1
    cents = abs(cents_signed)
    exact = [Decimal(cents) * pct / Decimal(100) for _, pct in weights]
    floors = [int(x.to_integral_value(rounding=ROUND_FLOOR)) for x in exact]
    leftover = cents - sum(floors)
    order = sorted(range(len(weights)), key=lambda i: (-(exact[i] - floors[i]), i))
    for i in order[:leftover]:
        floors[i] += 1
    return {code: q(Decimal(sign * f) / Decimal(100)) for (code, _), f in zip(weights, floors)}   # always 2 dp


@dataclass(frozen=True)
class IntercoLine:
    entity: str
    account_no: str
    debit: Decimal
    credit: Decimal
    memo: str


def interco_lines(
    net_by_entity: Mapping[str, Decimal],
    paying_entity: str,
    due_from_account: str,
    due_to_account: str,
) -> list[IntercoLine]:
    """Make every entity balance on its own by routing the difference through the paying entity.

    `net_by_entity` is debits minus credits per entity *before* inter-entity lines. An entity with
    excess debits (e.g. the School's share of payroll expense) books a credit to "Due to <payer>",
    and the payer books the mirror debit to "Due from <entity>". The payer's own net ends up zero
    whenever the journal as a whole balances.
    """
    out: list[IntercoLine] = []
    for entity, net in net_by_entity.items():
        if entity == paying_entity or net == ZERO:
            continue
        amount = abs(net)
        if net > 0:   # entity carries more expense than it paid for -> it owes the payer
            out.append(IntercoLine(entity, due_to_account, ZERO, amount, f"Due to {paying_entity} - payroll allocation"))
            out.append(IntercoLine(paying_entity, due_from_account, amount, ZERO, f"Due from {entity} - payroll allocation"))
        else:         # entity paid for more than it expensed -> the payer owes it
            out.append(IntercoLine(entity, due_from_account, amount, ZERO, f"Due from {paying_entity} - payroll allocation"))
            out.append(IntercoLine(paying_entity, due_to_account, ZERO, amount, f"Due to {entity} - payroll allocation"))
    return out
