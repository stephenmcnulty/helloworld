"""Append-only audit log with a hash chain.

Every entry stores the hash of the previous entry, so editing or deleting an old row is detectable
with `verify_chain`. SQLite triggers (see db.py) additionally reject UPDATE/DELETE. A database
administrator can still rebuild the whole chain; for production, ship entries to an external
write-once store (SIEM / object-lock bucket) as well.
"""
from __future__ import annotations

import hashlib
import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Mapping

GENESIS = "0" * 64


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _canonical(fields: Mapping[str, Any]) -> str:
    return json.dumps(fields, sort_keys=True, separators=(",", ":"), default=str)


def _entry_hash(prev_hash: str, fields: Mapping[str, Any]) -> str:
    return hashlib.sha256((prev_hash + "\n" + _canonical(fields)).encode("utf-8")).hexdigest()


def record(
    conn: sqlite3.Connection,
    *,
    actor: Mapping[str, Any] | None,
    action: str,
    client_id: str | None = None,
    job_id: int | None = None,
    mapping_version: int | None = None,
    file_sha256: str | None = None,
    details: Mapping[str, Any] | None = None,
) -> int:
    """Append one entry. Must be called inside Database.tx() so it commits with the action itself."""
    actor = actor or {"email": "system", "name": "system", "roles": []}
    fields = {
        "ts": _now(),
        "actor_email": actor.get("email", "unknown"),
        "actor_name": actor.get("name", ""),
        "actor_roles": ",".join(sorted(actor.get("roles", []))),
        "action": action,
        "client_id": client_id,
        "job_id": job_id,
        "mapping_version": mapping_version,
        "file_sha256": file_sha256,
        "details": _canonical(details or {}),
    }
    row = conn.execute("SELECT entry_hash FROM audit_log ORDER BY id DESC LIMIT 1").fetchone()
    prev_hash = row["entry_hash"] if row else GENESIS
    entry_hash = _entry_hash(prev_hash, fields)
    cur = conn.execute(
        """INSERT INTO audit_log (ts, actor_email, actor_name, actor_roles, action, client_id, job_id,
                                  mapping_version, file_sha256, details, prev_hash, entry_hash)
           VALUES (:ts, :actor_email, :actor_name, :actor_roles, :action, :client_id, :job_id,
                   :mapping_version, :file_sha256, :details, :prev_hash, :entry_hash)""",
        {**fields, "prev_hash": prev_hash, "entry_hash": entry_hash},
    )
    return int(cur.lastrowid)


@dataclass(frozen=True)
class ChainStatus:
    ok: bool
    entries: int
    broken_at: int | None = None


_HASHED_COLUMNS = (
    "ts", "actor_email", "actor_name", "actor_roles", "action", "client_id",
    "job_id", "mapping_version", "file_sha256", "details",
)


def verify_chain(conn: sqlite3.Connection) -> ChainStatus:
    prev = GENESIS
    count = 0
    for row in conn.execute("SELECT * FROM audit_log ORDER BY id"):
        count += 1
        fields = {k: row[k] for k in _HASHED_COLUMNS}
        if row["prev_hash"] != prev or row["entry_hash"] != _entry_hash(prev, fields):
            return ChainStatus(False, count, int(row["id"]))
        prev = row["entry_hash"]
    return ChainStatus(True, count)


def list_entries(
    conn: sqlite3.Connection,
    *,
    limit: int = 200,
    offset: int = 0,
    action: str | None = None,
    actor: str | None = None,
    job_id: int | None = None,
) -> list[sqlite3.Row]:
    clauses, params = [], []
    if action:
        clauses.append("action = ?")
        params.append(action)
    if actor:
        clauses.append("actor_email LIKE ?")
        params.append(f"%{actor}%")
    if job_id is not None:
        clauses.append("job_id = ?")
        params.append(job_id)
    where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    params += [max(1, min(limit, 1000)), max(0, offset)]
    return conn.execute(
        f"SELECT * FROM audit_log {where} ORDER BY id DESC LIMIT ? OFFSET ?", params
    ).fetchall()


def distinct_actions(conn: sqlite3.Connection) -> list[str]:
    return [r["action"] for r in conn.execute("SELECT DISTINCT action FROM audit_log ORDER BY action")]
