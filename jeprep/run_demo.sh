#!/usr/bin/env bash
# Start the demo with fake-user login and synthetic data. NEVER use this with real data.
set -euo pipefail
cd "$(dirname "$0")"
export DEMO_MODE=true
exec python -m uvicorn app.main:create_app --factory --host "${HOST:-127.0.0.1}" --port "${PORT:-8000}" "$@"
