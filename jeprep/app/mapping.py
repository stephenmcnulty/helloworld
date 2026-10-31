"""Mapping persistence: drafts, submission, approval and immutable version numbers.

Lifecycle:  draft --submit--> submitted --approve--> approved (gets the next version number)
                                          \\--reject--> rejected
Only `approved` rows are ever used to build a journal.
"""
from __future__ import annotations

import json
import sqlite3
from typing import Sequence

from .domain import MappingLine
from .money import ZERO  # noqa: F401  (re-export convenience for callers)
from .audit import _now


class MappingError(ValueError):
    pass


def lines_of(row: sqlite3.Row) -> list[MappingLine]:
    return [MappingLine.from_dict(d) for d in json.loads(row["lines_json"])]


def get_mapping(conn: sqlite3.Connection, mapping_id: int | None) -> sqlite3.Row | None:
    if mapping_id is None:
        return None
    return conn.execute("SELECT * FROM mappings WHERE id = ?", (mapping_id,)).fetchone()


def find_approved(conn: sqlite3.Connection, client_id: str, report_type: str, signature: str) -> sqlite3.Row | None:
    """Latest approved version whose layout signature matches exactly."""
    return conn.execute(
        """SELECT * FROM mappings WHERE client_id = ? AND report_type = ? AND status = 'approved'
           AND layout_signature = ? ORDER BY version DESC LIMIT 1""",
        (client_id, report_type, signature),
    ).fetchone()


def approved_versions(conn: sqlite3.Connection, client_id: str, report_type: str) -> list[sqlite3.Row]:
    return conn.execute(
        "SELECT * FROM mappings WHERE client_id = ? AND report_type = ? AND status = 'approved' ORDER BY version DESC",
        (client_id, report_type),
    ).fetchall()


def create_draft(
    conn: sqlite3.Connection, *, job_id: int | None, client_id: str, report_type: str, signature: str,
    headers: Sequence[str], lines: Sequence[MappingLine], source: str, notice: str, user_email: str,
) -> int:
    cur = conn.execute(
        """INSERT INTO mappings (client_id, report_type, status, layout_signature, headers_json, lines_json,
                                 source, notice, job_id, created_by, created_at)
           VALUES (?, ?, 'draft', ?, ?, ?, ?, ?, ?, ?, ?)""",
        (client_id, report_type, signature, json.dumps(list(headers)),
         json.dumps([l.to_dict() for l in lines]), source, notice, job_id, user_email, _now()),
    )
    return int(cur.lastrowid)


def save_draft(conn: sqlite3.Connection, mapping_id: int, lines: Sequence[MappingLine], *,
               source: str | None = None, notice: str | None = None) -> None:
    row = get_mapping(conn, mapping_id)
    if row is None or row["status"] != "draft":
        raise MappingError("Only a draft mapping can be edited.")
    conn.execute(
        "UPDATE mappings SET lines_json = ?, source = COALESCE(?, source), notice = COALESCE(?, notice) WHERE id = ?",
        (json.dumps([l.to_dict() for l in lines]), source, notice, mapping_id),
    )


def submit(conn: sqlite3.Connection, mapping_id: int, user_email: str) -> None:
    row = get_mapping(conn, mapping_id)
    if row is None or row["status"] != "draft":
        raise MappingError("Only a draft mapping can be submitted.")
    conn.execute(
        "UPDATE mappings SET status = 'submitted', submitted_by = ?, submitted_at = ? WHERE id = ?",
        (user_email, _now(), mapping_id),
    )


def reopen(conn: sqlite3.Connection, mapping_id: int) -> None:
    """A rejected (or submitted-but-withdrawn) mapping goes back to draft so the preparer can fix it."""
    conn.execute("UPDATE mappings SET status = 'draft', decided_by = NULL, decided_at = NULL WHERE id = ? "
                 "AND status IN ('rejected', 'submitted')", (mapping_id,))


def approve(conn: sqlite3.Connection, mapping_id: int, approver_email: str) -> int:
    row = get_mapping(conn, mapping_id)
    if row is None or row["status"] != "submitted":
        raise MappingError("Only a submitted mapping can be approved.")
    version = conn.execute(
        "SELECT COALESCE(MAX(version), 0) + 1 AS v FROM mappings WHERE client_id = ? AND report_type = ?",
        (row["client_id"], row["report_type"]),
    ).fetchone()["v"]
    conn.execute(
        "UPDATE mappings SET status = 'approved', version = ?, decided_by = ?, decided_at = ? WHERE id = ?",
        (version, approver_email, _now(), mapping_id),
    )
    return int(version)


def reject(conn: sqlite3.Connection, mapping_id: int, reviewer_email: str, note: str) -> None:
    row = get_mapping(conn, mapping_id)
    if row is None or row["status"] != "submitted":
        raise MappingError("Only a submitted mapping can be rejected.")
    conn.execute(
        "UPDATE mappings SET status = 'rejected', decided_by = ?, decided_at = ?, decision_note = ? WHERE id = ?",
        (reviewer_email, _now(), note[:500], mapping_id),
    )


def merge_missing(base: Sequence[MappingLine], additions: Sequence[MappingLine]) -> list[MappingLine]:
    """Fill only the *unassigned* lines of `base` from `additions`; never overwrite a human or rule choice."""
    extra = {l.source_column: l for l in additions}
    return [extra[l.source_column] if (not l.role and l.source_column in extra) else l for l in base]
