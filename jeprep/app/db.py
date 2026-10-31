"""SQLite access. Plain sqlite3, explicit transactions, one short-lived connection per unit of work."""
from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

SCHEMA = """
CREATE TABLE IF NOT EXISTS clients (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    active INTEGER NOT NULL DEFAULT 1,
    due_from_account TEXT NOT NULL DEFAULT '',
    due_to_account TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS client_entities (
    client_id TEXT NOT NULL REFERENCES clients(id),
    code TEXT NOT NULL,
    name TEXT NOT NULL,
    alloc_pct TEXT NOT NULL DEFAULT '0',
    is_paying INTEGER NOT NULL DEFAULT 0,
    default_fund TEXT NOT NULL DEFAULT '',
    PRIMARY KEY (client_id, code)
);

CREATE TABLE IF NOT EXISTS client_funds (
    client_id TEXT NOT NULL REFERENCES clients(id),
    code TEXT NOT NULL,
    name TEXT NOT NULL,
    PRIMARY KEY (client_id, code)
);

CREATE TABLE IF NOT EXISTS gl_accounts (
    client_id TEXT NOT NULL REFERENCES clients(id),
    account_no TEXT NOT NULL,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    PRIMARY KEY (client_id, account_no)
);

-- A mapping row is either a draft/submitted proposal (version NULL) or an approved, immutable version.
CREATE TABLE IF NOT EXISTS mappings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id TEXT NOT NULL REFERENCES clients(id),
    report_type TEXT NOT NULL,
    version INTEGER,
    status TEXT NOT NULL CHECK (status IN ('draft','submitted','approved','rejected')),
    layout_signature TEXT NOT NULL,
    headers_json TEXT NOT NULL,
    lines_json TEXT NOT NULL,
    source TEXT NOT NULL DEFAULT 'manual',
    notice TEXT NOT NULL DEFAULT '',
    job_id INTEGER,
    created_by TEXT NOT NULL,
    created_at TEXT NOT NULL,
    submitted_by TEXT,
    submitted_at TEXT,
    decided_by TEXT,
    decided_at TEXT,
    decision_note TEXT NOT NULL DEFAULT '',
    UNIQUE (client_id, report_type, version)
);

CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id TEXT NOT NULL REFERENCES clients(id),
    target_system TEXT NOT NULL CHECK (target_system IN ('intacct','qbo')),
    report_type TEXT NOT NULL,
    period_start TEXT NOT NULL,
    period_end TEXT NOT NULL,
    allocate INTEGER NOT NULL DEFAULT 0,
    status TEXT NOT NULL,
    created_by TEXT NOT NULL,
    created_by_name TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    file_name TEXT,
    file_ext TEXT,
    file_stored TEXT,
    file_sha256 TEXT,
    file_size INTEGER,
    file_uploaded_by TEXT,
    file_uploaded_at TEXT,
    file_deleted_at TEXT,
    file_delete_reason TEXT,
    layout_signature TEXT,
    mapping_id INTEGER REFERENCES mappings(id),
    draft_mapping_id INTEGER REFERENCES mappings(id),
    je_hash TEXT,
    export_requested_by TEXT,
    export_requested_at TEXT,
    export_approved_by TEXT,
    export_approved_at TEXT,
    exported_by TEXT,
    exported_at TEXT,
    export_name TEXT,
    export_stored TEXT,
    export_sha256 TEXT,
    export_deleted_at TEXT,
    delete_after_export INTEGER NOT NULL DEFAULT 0
);

-- Append-only, hash-chained audit trail (see app/audit.py).
CREATE TABLE IF NOT EXISTS audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts TEXT NOT NULL,
    actor_email TEXT NOT NULL,
    actor_name TEXT NOT NULL,
    actor_roles TEXT NOT NULL,
    action TEXT NOT NULL,
    client_id TEXT,
    job_id INTEGER,
    mapping_version INTEGER,
    file_sha256 TEXT,
    details TEXT NOT NULL,
    prev_hash TEXT NOT NULL,
    entry_hash TEXT NOT NULL
);

CREATE TRIGGER IF NOT EXISTS audit_log_no_update BEFORE UPDATE ON audit_log
BEGIN SELECT RAISE(ABORT, 'audit_log is append-only'); END;
CREATE TRIGGER IF NOT EXISTS audit_log_no_delete BEFORE DELETE ON audit_log
BEGIN SELECT RAISE(ABORT, 'audit_log is append-only'); END;

CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs(status);
CREATE INDEX IF NOT EXISTS idx_mappings_lookup ON mappings(client_id, report_type, status, version);
CREATE INDEX IF NOT EXISTS idx_audit_action ON audit_log(action);
"""


class Database:
    def __init__(self, path: Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def connect(self) -> sqlite3.Connection:
        # isolation_level=None -> we issue BEGIN/COMMIT ourselves (see tx()).
        conn = sqlite3.connect(self.path, isolation_level=None, timeout=10, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("PRAGMA journal_mode = WAL")
        return conn

    def init_schema(self) -> None:
        conn = self.connect()
        try:
            conn.executescript(SCHEMA)
        finally:
            conn.close()
        # The database holds client financial data: owner-only permissions.
        try:
            self.path.chmod(0o600)
        except OSError:
            pass

    @contextmanager
    def tx(self) -> Iterator[sqlite3.Connection]:
        """Write transaction. BEGIN IMMEDIATE serialises writers, which the audit hash chain relies on."""
        conn = self.connect()
        try:
            conn.execute("BEGIN IMMEDIATE")
            try:
                yield conn
            except BaseException:
                conn.execute("ROLLBACK")
                raise
            else:
                conn.execute("COMMIT")
        finally:
            conn.close()

    @contextmanager
    def read(self) -> Iterator[sqlite3.Connection]:
        conn = self.connect()
        try:
            yield conn
        finally:
            conn.close()
