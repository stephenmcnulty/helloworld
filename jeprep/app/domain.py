"""Domain objects shared by the engine and the web layer: client configuration and mapping lines."""
from __future__ import annotations

import sqlite3
from dataclasses import asdict, dataclass, field, fields
from decimal import Decimal

REPORT_TYPES = {"payroll_register": "Payroll Register"}
TARGET_SYSTEMS = {"intacct": "Sage Intacct", "qbo": "QuickBooks Online"}

ROLES = ("amount", "employee_name", "employee_id", "department", "pay_date", "ignore")
ROLE_LABELS = {
    "amount": "Amount → journal line",
    "employee_name": "Employee name",
    "employee_id": "Employee ID",
    "department": "Department",
    "pay_date": "Pay date",
    "ignore": "Ignore (not posted)",
}
LINE_TYPES = ("expense", "liability", "cash", "asset", "other")
SIDES = ("debit", "credit")


@dataclass(frozen=True)
class Account:
    account_no: str
    name: str
    category: str


@dataclass(frozen=True)
class Entity:
    code: str
    name: str
    alloc_pct: Decimal
    is_paying: bool
    default_fund: str


@dataclass
class ClientConfig:
    id: str
    name: str
    description: str = ""
    active: bool = True
    due_from_account: str = ""
    due_to_account: str = ""
    entities: list[Entity] = field(default_factory=list)
    funds: dict[str, str] = field(default_factory=dict)          # code -> name
    accounts: dict[str, Account] = field(default_factory=dict)   # account_no -> Account

    @property
    def paying_entity(self) -> Entity | None:
        for e in self.entities:
            if e.is_paying:
                return e
        return self.entities[0] if self.entities else None

    @property
    def entity_codes(self) -> list[str]:
        return [e.code for e in self.entities]

    def entity(self, code: str) -> Entity | None:
        return next((e for e in self.entities if e.code == code), None)

    def allocation_problems(self) -> list[str]:
        """Why allocation can't be used for this client (empty list == ready)."""
        problems: list[str] = []
        if len(self.entities) < 2:
            problems.append("fewer than two entities are configured")
        total = sum((e.alloc_pct for e in self.entities), Decimal("0"))
        if total != Decimal("100"):
            problems.append(f"allocation percentages add up to {total}%, not 100%")
        if sum(1 for e in self.entities if e.is_paying) != 1:
            problems.append("exactly one entity must be marked as the paying entity")
        for label, acct in (("due-from", self.due_from_account), ("due-to", self.due_to_account)):
            if acct not in self.accounts:
                problems.append(f"the {label} (inter-entity) account is not set to a valid GL account")
        return problems

    def account_for_category(self, category: str) -> str:
        for no in sorted(self.accounts):
            if self.accounts[no].category == category:
                return no
        return ""

    def line_type_for(self, account_no: str) -> str:
        """Derive the line type from the account's category so type and account can never disagree."""
        acct = self.accounts.get(account_no)
        if acct is None:
            return ""
        if acct.category.endswith("_expense"):
            return "expense"
        if acct.category == "cash":
            return "cash"
        if acct.category in ("due_from",):
            return "asset"
        if acct.category.endswith("_payable") or acct.category == "due_to":
            return "liability"
        return "other"

    def default_fund_for(self, entity_code: str) -> str:
        ent = self.entity(entity_code)
        if ent and ent.default_fund in self.funds:
            return ent.default_fund
        return next(iter(self.funds), "")


def load_client(conn: sqlite3.Connection, client_id: str) -> ClientConfig | None:
    row = conn.execute("SELECT * FROM clients WHERE id = ?", (client_id,)).fetchone()
    if row is None:
        return None
    cfg = ClientConfig(
        id=row["id"],
        name=row["name"],
        description=row["description"],
        active=bool(row["active"]),
        due_from_account=row["due_from_account"],
        due_to_account=row["due_to_account"],
    )
    for e in conn.execute("SELECT * FROM client_entities WHERE client_id = ? ORDER BY rowid", (client_id,)):
        cfg.entities.append(
            Entity(e["code"], e["name"], Decimal(e["alloc_pct"]), bool(e["is_paying"]), e["default_fund"])
        )
    for f in conn.execute("SELECT * FROM client_funds WHERE client_id = ? ORDER BY rowid", (client_id,)):
        cfg.funds[f["code"]] = f["name"]
    for a in conn.execute("SELECT * FROM gl_accounts WHERE client_id = ? ORDER BY account_no", (client_id,)):
        cfg.accounts[a["account_no"]] = Account(a["account_no"], a["name"], a["category"])
    return cfg


def list_clients(conn: sqlite3.Connection, *, active_only: bool = True) -> list[sqlite3.Row]:
    sql = "SELECT * FROM clients" + (" WHERE active = 1" if active_only else "") + " ORDER BY name"
    return conn.execute(sql).fetchall()


@dataclass
class MappingLine:
    """One report column and what it becomes. Role '' means 'not yet assigned' (counts as unmapped)."""

    source_column: str
    role: str = ""
    line_type: str = ""
    side: str = ""
    gl_account: str = ""
    entity: str = ""
    fund: str = ""
    offset_account: str = ""   # optional credit/debit-opposite account, e.g. employer tax -> payable
    memo: str = ""
    origin: str = "manual"     # rules | ai | mock | manual | saved
    confidence: float | None = None
    rationale: str = ""
    reviewed: bool = False

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "MappingLine":
        known = {f.name for f in fields(cls)}
        return cls(**{k: v for k, v in data.items() if k in known})

    @property
    def needs_human_review(self) -> bool:
        """AI and mock suggestions must be ticked off line by line before a mapping can be submitted."""
        return self.origin in {"ai", "mock"} and not self.reviewed

    def problems(self, client: ClientConfig) -> list[str]:
        """Reasons this line cannot be posted (empty == complete and valid)."""
        if not self.role:
            return ["no role assigned"]
        if self.role not in ROLES:
            return [f"unknown role {self.role!r}"]
        if self.role != "amount":
            return []
        out: list[str] = []
        if self.line_type not in LINE_TYPES:
            out.append("line type missing")
        if self.side not in SIDES:
            out.append("debit/credit side missing")
        if not self.gl_account:
            out.append("GL account missing")
        elif self.gl_account not in client.accounts:
            out.append(f"GL account {self.gl_account} is not in the client's chart of accounts")
        if self.offset_account and self.offset_account not in client.accounts:
            out.append(f"offset account {self.offset_account} is not in the client's chart of accounts")
        if not self.entity:
            out.append("entity missing")
        elif client.entity(self.entity) is None:
            out.append(f"entity {self.entity} is not configured for this client")
        if not self.fund:
            out.append("fund missing")
        elif self.fund not in client.funds:
            out.append(f"fund {self.fund} is not configured for this client")
        return out

    def is_postable(self, client: ClientConfig) -> bool:
        return self.role == "amount" and not self.problems(client)


def save_client(conn: sqlite3.Connection, cfg: ClientConfig, *, replace_chart: bool = True) -> None:
    """Upsert a client with its entities, funds and (optionally) chart of accounts."""
    from .audit import _now

    conn.execute(
        """INSERT INTO clients (id, name, description, active, due_from_account, due_to_account, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?)
           ON CONFLICT(id) DO UPDATE SET name = excluded.name, description = excluded.description,
               active = excluded.active, due_from_account = excluded.due_from_account,
               due_to_account = excluded.due_to_account""",
        (cfg.id, cfg.name, cfg.description, int(cfg.active), cfg.due_from_account, cfg.due_to_account, _now()),
    )
    conn.execute("DELETE FROM client_entities WHERE client_id = ?", (cfg.id,))
    for e in cfg.entities:
        conn.execute(
            "INSERT INTO client_entities (client_id, code, name, alloc_pct, is_paying, default_fund) VALUES (?, ?, ?, ?, ?, ?)",
            (cfg.id, e.code, e.name, str(e.alloc_pct), int(e.is_paying), e.default_fund),
        )
    conn.execute("DELETE FROM client_funds WHERE client_id = ?", (cfg.id,))
    for code, name in cfg.funds.items():
        conn.execute("INSERT INTO client_funds (client_id, code, name) VALUES (?, ?, ?)", (cfg.id, code, name))
    if replace_chart:
        conn.execute("DELETE FROM gl_accounts WHERE client_id = ?", (cfg.id,))
        for a in cfg.accounts.values():
            conn.execute(
                "INSERT INTO gl_accounts (client_id, account_no, name, category) VALUES (?, ?, ?, ?)",
                (cfg.id, a.account_no, a.name, a.category),
            )
