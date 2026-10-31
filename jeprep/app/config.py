"""Runtime configuration, read only from environment variables (and an optional local .env).

No secret has a default value that would be safe to ship: SECRET_KEY, OKTA_CLIENT_SECRET and
ANTHROPIC_API_KEY are only ever read from the environment.
"""
from __future__ import annotations

import os
import secrets
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

BASE_DIR = Path(__file__).resolve().parent.parent


class ConfigError(RuntimeError):
    """Raised at startup when the environment is unsafe or incomplete."""


def _as_bool(value: str | None, default: bool = False) -> bool:
    if value is None or value.strip() == "":
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _as_int(value: str | None, default: int) -> int:
    try:
        return int(value) if value not in (None, "") else default
    except ValueError as exc:
        raise ConfigError(f"Expected an integer, got {value!r}") from exc


def load_dotenv(path: Path, env: dict[str, str] | None = None) -> None:
    """Tiny .env loader (KEY=VALUE per line). Never overrides variables already set."""
    target = os.environ if env is None else env
    if not path.is_file():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        value = value.strip().strip("'\"")
        target.setdefault(key.strip(), value)


@dataclass(frozen=True)
class Settings:
    demo_mode: bool
    app_env: str
    secret_key: str
    data_dir: Path
    db_path: Path
    upload_dir: Path
    export_dir: Path
    max_upload_bytes: int
    max_rows: int
    max_columns: int
    retention_days: int
    delete_after_export_default: bool
    cookie_secure: bool
    okta_issuer: str
    okta_client_id: str
    okta_client_secret: str
    okta_redirect_uri: str
    okta_group_preparer: str
    okta_group_reviewer: str
    okta_group_admin: str
    anthropic_api_key: str
    anthropic_model: str

    @property
    def okta_configured(self) -> bool:
        return bool(self.okta_issuer and self.okta_client_id and self.okta_client_secret)

    @property
    def ai_configured(self) -> bool:
        return bool(self.anthropic_api_key)

    @classmethod
    def from_env(cls, env: Mapping[str, str] | None = None, *, validate: bool = True) -> "Settings":
        e = os.environ if env is None else env
        data_dir = Path(e.get("DATA_DIR") or BASE_DIR / "data").resolve()
        demo_mode = _as_bool(e.get("DEMO_MODE"), False)
        secret = e.get("SECRET_KEY", "")
        if not secret and demo_mode:
            # Demo only: a per-process key. Sessions are invalidated on every restart.
            secret = secrets.token_urlsafe(48)
        settings = cls(
            demo_mode=demo_mode,
            app_env=(e.get("APP_ENV") or "demo").lower(),
            secret_key=secret,
            data_dir=data_dir,
            db_path=Path(e.get("DB_PATH") or data_dir / "jeprep.sqlite3").resolve(),
            upload_dir=data_dir / "uploads",
            export_dir=data_dir / "exports",
            max_upload_bytes=_as_int(e.get("MAX_UPLOAD_MB"), 5) * 1024 * 1024,
            max_rows=_as_int(e.get("MAX_ROWS"), 20000),
            max_columns=_as_int(e.get("MAX_COLUMNS"), 100),
            retention_days=_as_int(e.get("UPLOAD_RETENTION_DAYS"), 30),
            delete_after_export_default=_as_bool(e.get("DELETE_AFTER_EXPORT_DEFAULT"), True),
            cookie_secure=_as_bool(e.get("COOKIE_SECURE"), False),
            okta_issuer=(e.get("OKTA_ISSUER") or "").rstrip("/"),
            okta_client_id=e.get("OKTA_CLIENT_ID", ""),
            okta_client_secret=e.get("OKTA_CLIENT_SECRET", ""),
            okta_redirect_uri=e.get("OKTA_REDIRECT_URI", ""),
            okta_group_preparer=e.get("OKTA_GROUP_PREPARER", "JE-Preparer"),
            okta_group_reviewer=e.get("OKTA_GROUP_REVIEWER", "JE-Reviewer"),
            okta_group_admin=e.get("OKTA_GROUP_ADMIN", "JE-Admin"),
            anthropic_api_key=e.get("ANTHROPIC_API_KEY", ""),
            anthropic_model=e.get("ANTHROPIC_MODEL", "claude-opus-5-5"),
        )
        if validate:
            settings.validate()
        return settings

    def validate(self) -> None:
        if self.demo_mode and self.app_env == "production":
            raise ConfigError("DEMO_MODE=true is not allowed when APP_ENV=production.")
        if not self.demo_mode and not self.okta_configured:
            raise ConfigError(
                "Authentication is not configured. Either set DEMO_MODE=true (fake users, demo only) "
                "or set OKTA_ISSUER, OKTA_CLIENT_ID and OKTA_CLIENT_SECRET."
            )
        if not self.secret_key or len(self.secret_key) < 32:
            raise ConfigError("SECRET_KEY must be set (at least 32 characters) when DEMO_MODE is off.")
