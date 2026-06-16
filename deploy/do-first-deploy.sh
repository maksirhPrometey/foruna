#!/usr/bin/env bash
# FortunaPrint — перший деплой на DigitalOcean Droplet
# Запуск: bash deploy/do-first-deploy.sh
set -euo pipefail

APP_DIR="/opt/fortuna"
REPO="https://github.com/maksirhPrometey/foruna.git"
COMPOSE="docker compose -f docker-compose.yml -f docker-compose.prod.yml"

# ── 1. Docker ──────────────────────────────────────────────────────────────────
if ! command -v docker &>/dev/null; then
    echo "==> Installing Docker..."
    curl -fsSL https://get.docker.com | sh
    systemctl enable --now docker
fi
echo "==> Docker: $(docker --version)"

# ── 2. Репо ───────────────────────────────────────────────────────────────────
if [ ! -d "${APP_DIR}/.git" ]; then
    git clone "${REPO}" "${APP_DIR}"
fi
cd "${APP_DIR}"
git pull origin main

# ── 3. .env (тестові значення — замінити перед production) ────────────────────
if [ ! -f .env ]; then
cat > .env <<'EOF'
DJANGO_SETTINGS_MODULE=config.settings.production
SECRET_KEY=dbXK3NY-iA7wUb5ZEw7cuDf7Er4gllZLR7Dz0YVV94bUN8YwR8ZjSBg2skET4dRAKyM
DEBUG=False

POSTGRES_DB=fortunaprint
POSTGRES_USER=fortunaprint
POSTGRES_PASSWORD=tl7lCbAROJy1x9eRT6HygvLqDL7X
DB_HOST=db
DB_PORT=5432

ALLOWED_HOSTS=46.101.191.189,fortprint.com.ua,www.fortprint.com.ua
CSRF_TRUSTED_ORIGINS=http://46.101.191.189,https://fortprint.com.ua,https://www.fortprint.com.ua
SECURE_SSL_REDIRECT=False

TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
EOF
    echo "==> .env створено"
else
    echo "==> .env вже існує — пропускаємо"
fi

# ── 4. Build + запуск ─────────────────────────────────────────────────────────
echo "==> Building images..."
${COMPOSE} build

echo "==> Starting services..."
${COMPOSE} up -d

echo "==> Waiting for backend..."
sleep 15

# ── 5. Seed контент + зображення ─────────────────────────────────────────────
echo "==> Seed: текстовий контент..."
${COMPOSE} exec backend python manage.py seed_production

echo "==> Seed: зображення продуктів та логотипи..."
${COMPOSE} exec backend python manage.py seed_images

# ── 6. Superuser ──────────────────────────────────────────────────────────────
echo ""
echo "==> Створення суперкористувача (введи логін/пароль для /admin/):"
${COMPOSE} exec backend python manage.py createsuperuser

# ── 6. Статус ─────────────────────────────────────────────────────────────────
echo ""
${COMPOSE} ps

echo ""
echo "=== Готово ==="
echo "Сайт:   http://46.101.191.189"
echo "Адмін:  http://46.101.191.189/admin/"
echo "Health: http://46.101.191.189/healthz/"
