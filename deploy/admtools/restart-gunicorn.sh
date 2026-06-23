#!/bin/bash
# Перезапуск Gunicorn на ADM.TOOLS — один процес на IP з панелі «Проксирование».
# Запуск: bash deploy/admtools/restart-gunicorn.sh
# Або: bash restart-gunicorn.sh  (з кореня проєкту)
set -euo pipefail

APP_DIR="/home/ep616268/fortprint.com.ua"
# IP:PORT з панелі ADM.TOOLS → Проксирование HTTP-трафика (НЕ 127.0.0.1)
BIND="${GUNICORN_BIND:-127.1.9.16:3000}"

cd "${APP_DIR}"

echo "=== Зупинка всіх gunicorn config.wsgi ==="
pkill -f "gunicorn config.wsgi:application" 2>/dev/null || true
sleep 2

if pgrep -f "gunicorn config.wsgi:application" >/dev/null; then
    echo "ПОМИЛКА: gunicorn ще працює. Зупиніть у панелі ADM.TOOLS → Зупинити"
    pgrep -af "gunicorn config.wsgi"
    exit 1
fi

echo "=== Старт gunicorn на ${BIND} ==="
echo "У панелі має бути та сама команда bind!"
exec .venv/bin/gunicorn config.wsgi:application \
    --bind "${BIND}" \
    --workers 2 \
    --timeout 120
