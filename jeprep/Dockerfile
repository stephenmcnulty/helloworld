# Journal Entry Prep (demo). Build context is this folder (jeprep/).
#   docker build -t journal-entry-prep .
#   docker run -p 8000:8000 -e ACCESS_CODE=choose-a-code journal-entry-prep      # then http://localhost:8000
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Dependencies first so this layer is cached when only the code changes.
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app ./app
COPY demo_data ./demo_data

# Run as an unprivileged user; it only needs to write the database, uploads and exports under /app/data.
RUN useradd --system --uid 10001 --home-dir /app appuser \
    && mkdir -p /app/data \
    && chown -R appuser /app/data /app/demo_data
USER appuser

# Demo defaults. Set COOKIE_SECURE=true when served over HTTPS (any real host), and ACCESS_CODE for anything others can reach.
ENV DEMO_MODE=true \
    APP_ENV=demo \
    DATA_DIR=/app/data \
    COOKIE_SECURE=false \
    PORT=8000

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=6s --start-period=20s --retries=3 CMD ["python", "-m", "app.healthcheck"]

# One worker only (SQLite). Hosts set $PORT; --proxy-headers makes the real client address visible behind
# the host's HTTPS proxy. Trusting every forwarded address is correct only because the host's proxy is the
# sole way in; do not publish this container's port directly to the internet.
CMD ["sh", "-c", "exec python -m uvicorn app.main:create_app --factory --host 0.0.0.0 --port ${PORT:-8000} --proxy-headers --forwarded-allow-ips='*'"]
