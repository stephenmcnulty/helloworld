"""Upload validation and local file storage (restricted permissions, retention, delete-after-export)."""
from __future__ import annotations

import hashlib
import os
import re
import uuid
import zipfile
import io
from datetime import datetime, timedelta, timezone
from pathlib import Path

from . import audit
from .config import Settings
from .db import Database

ALLOWED_EXTENSIONS = (".csv", ".xlsx")
MAX_UNCOMPRESSED_BYTES = 60 * 1024 * 1024   # zip-bomb guard for .xlsx
_BINARY_PREFIXES = (b"PK\x03\x04", b"%PDF", b"MZ", b"\x7fELF", b"\xd0\xcf\x11\xe0", b"GIF8", b"\x89PNG", b"\xff\xd8\xff")


class UploadError(ValueError):
    """Rejected upload; the message is safe to show to the user."""


def sanitize_filename(name: str) -> str:
    base = os.path.basename((name or "").replace("\\", "/"))
    base = re.sub(r"[\x00-\x1f\x7f]", "", base).strip().strip(".")
    return base[:120] or "upload"


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def validate_upload(filename: str, data: bytes, max_bytes: int) -> str:
    """Check extension, size and content type; returns the (lower-case) extension."""
    ext = os.path.splitext(sanitize_filename(filename))[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise UploadError("Only .csv and .xlsx files are accepted.")
    if not data:
        raise UploadError("The file is empty.")
    if len(data) > max_bytes:
        raise UploadError(f"The file is larger than the {max_bytes // (1024 * 1024)} MB limit.")
    if ext == ".csv":
        if b"\x00" in data[:65536] or data.startswith(_BINARY_PREFIXES):
            raise UploadError("This does not look like a CSV text file.")
    else:
        _validate_xlsx(data)
    return ext


def _validate_xlsx(data: bytes) -> None:
    if not data.startswith(b"PK\x03\x04"):
        raise UploadError("This does not look like an .xlsx workbook.")
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as zf:
            infos = zf.infolist()
            names = {i.filename for i in infos}
            if "[Content_Types].xml" not in names or "xl/workbook.xml" not in names:
                raise UploadError("This does not look like an .xlsx workbook.")
            if any(".." in n.split("/") or n.startswith("/") for n in names):
                raise UploadError("The workbook contains unsafe paths.")
            if any("vbaproject" in n.lower() for n in names):
                raise UploadError("Workbooks with macros are not accepted. Save a copy as a plain .xlsx.")
            if sum(i.file_size for i in infos) > MAX_UNCOMPRESSED_BYTES:
                raise UploadError("The workbook expands to an unreasonable size.")
    except zipfile.BadZipFile as exc:
        raise UploadError("This does not look like an .xlsx workbook.") from exc


def ensure_private_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    try:
        path.chmod(0o700)
    except OSError:
        pass


def store_bytes(base_dir: Path, subdir: str, data: bytes, ext: str) -> str:
    """Write under a random name (never the user's filename) with owner-only permissions."""
    folder = base_dir / subdir
    ensure_private_dir(base_dir)
    ensure_private_dir(folder)
    name = f"{uuid.uuid4().hex}{ext}"
    fd = os.open(folder / name, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "wb") as fh:
        fh.write(data)
    return f"{subdir}/{name}"


def resolve_stored(base_dir: Path, stored: str) -> Path:
    path = (base_dir / stored).resolve()
    if base_dir.resolve() not in path.parents:
        raise UploadError("Invalid stored file path.")
    return path


def read_stored(base_dir: Path, stored: str) -> bytes:
    return resolve_stored(base_dir, stored).read_bytes()


def delete_stored(base_dir: Path, stored: str | None) -> bool:
    if not stored:
        return False
    path = resolve_stored(base_dir, stored)
    try:
        path.unlink()
    except FileNotFoundError:
        return False
    try:
        path.parent.rmdir()   # remove the per-job folder once empty
    except OSError:
        pass
    return True


def purge_expired(settings: Settings, db: Database, *, now: datetime | None = None,
                  actor: dict | None = None) -> list[dict]:
    """Delete uploaded and exported files older than the retention window. Returns what was removed."""
    now = now or datetime.now(timezone.utc)
    cutoff = (now - timedelta(days=settings.retention_days)).isoformat(timespec="seconds")
    removed: list[dict] = []
    with db.tx() as conn:
        for job in conn.execute(
            "SELECT * FROM jobs WHERE file_stored IS NOT NULL AND file_deleted_at IS NULL AND file_uploaded_at < ?", (cutoff,)
        ).fetchall():
            delete_stored(settings.upload_dir, job["file_stored"])
            conn.execute("UPDATE jobs SET file_deleted_at = ?, file_delete_reason = 'retention', file_stored = NULL WHERE id = ?",
                         (now.isoformat(timespec="seconds"), job["id"]))
            audit.record(conn, actor=actor, action="file_deleted", client_id=job["client_id"], job_id=job["id"],
                         file_sha256=job["file_sha256"], details={"reason": "retention", "kind": "upload",
                                                                    "retention_days": settings.retention_days})
            removed.append({"job_id": job["id"], "kind": "upload"})
        for job in conn.execute(
            "SELECT * FROM jobs WHERE export_stored IS NOT NULL AND export_deleted_at IS NULL AND exported_at < ?", (cutoff,)
        ).fetchall():
            delete_stored(settings.export_dir, job["export_stored"])
            conn.execute("UPDATE jobs SET export_deleted_at = ?, export_stored = NULL WHERE id = ?",
                         (now.isoformat(timespec="seconds"), job["id"]))
            audit.record(conn, actor=actor, action="file_deleted", client_id=job["client_id"], job_id=job["id"],
                         file_sha256=job["export_sha256"], details={"reason": "retention", "kind": "export",
                                                                      "retention_days": settings.retention_days})
            removed.append({"job_id": job["id"], "kind": "export"})
    return removed
