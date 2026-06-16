#!/usr/bin/env bash
set -e

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate --noinput
touch passenger_wsgi.py 2>/dev/null || true
