"""Container health probe: exit 0 if the local server answers /healthz. Used by the Dockerfile HEALTHCHECK."""
import os
import sys
import urllib.request


def main() -> int:
    url = f"http://127.0.0.1:{os.environ.get('PORT', '8000')}/healthz"
    try:
        with urllib.request.urlopen(url, timeout=4) as resp:
            return 0 if resp.status == 200 else 1
    except Exception:
        return 1


if __name__ == "__main__":
    sys.exit(main())
