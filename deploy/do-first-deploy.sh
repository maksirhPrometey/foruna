#!/usr/bin/env bash
# FortunaPrint — перший деплой на DigitalOcean Droplet
# Запуск на сервері: bash do-first-deploy.sh
set -euo pipefail

REPO="https://github.com/maksirhPrometey/foruna.git"
APP_DIR="/opt/fortuna"
COMPOSE="docker compose -f docker-compose.yml -f docker-compose.prod.yml"

# ── 1. Docker ──────────────────────────────────────────────────────────────────
if ! command -v docker &>/dev/null; then
    echo "==> Installing Docker..."
    curl -fsSL https://get.docker.com | sh
    systemctl enable --now docker
fi

echo "==> Docker: $(docker --version)"

# ── 2. Клон репо ──────────────────────────────────────────────────────────────
if [ ! -d "${APP_DIR}/.git" ]; then
    git clone "${REPO}" "${APP_DIR}"
fi

cd "${APP_DIR}"
git pull origin main

# ── 3. .env ───────────────────────────────────────────────────────────────────
if [ ! -f .env ]; then
    cp .env.production .env
    echo "==> .env створено з .env.production"
fi

# ── 4. Build + запуск ─────────────────────────────────────────────────────────
echo "==> Building images..."
${COMPOSE} build

echo "==> Starting services..."
${COMPOSE} up -d

echo "==> Waiting for backend to be healthy..."
sleep 10

# ── 5. Superuser ──────────────────────────────────────────────────────────────
echo ""
echo "==> Створення суперкористувача:"
${COMPOSE} exec backend python manage.py createsuperuser

# ── 6. Перевірка ──────────────────────────────────────────────────────────────
echo ""
echo "==> Статус контейнерів:"
${COMPOSE} ps

echo ""
echo "=== Готово ==="
echo "Сайт:   http://46.101.191.189"
echo "Адмін:  http://46.101.191.189/admin/"
echo "Health: http://46.101.191.189/healthz/"
