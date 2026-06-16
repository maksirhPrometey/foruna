#!/usr/bin/env bash
set -euo pipefail

echo "==> Waiting for PostgreSQL..."
python - <<'PY'
import os, sys, time
import psycopg2

host = os.environ.get("DB_HOST", "db")
port = os.environ.get("DB_PORT", "5432")
for i in range(30):
    try:
        psycopg2.connect(
            dbname=os.environ["POSTGRES_DB"],
            user=os.environ["POSTGRES_USER"],
            password=os.environ["POSTGRES_PASSWORD"],
            host=host,
            port=port,
        )
        print("==> DB ready")
        sys.exit(0)
    except psycopg2.OperationalError:
        print(f"  waiting... ({i+1}/30)")
        time.sleep(2)
print("FATAL: DB not ready after 60s")
sys.exit(1)
PY

echo "==> migrate"
python manage.py migrate --noinput

echo "==> collectstatic"
python manage.py collectstatic --noinput

_count=$(find "${STATIC_ROOT:-/app/staticfiles}" -type f 2>/dev/null | wc -l | tr -d ' ')
echo "==> static files: ${_count}"

exec "$@"
