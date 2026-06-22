#!/bin/bash
# FortunaPrint — перший деплой на ADM.TOOLS (Ukraine.com.ua)
# Запуск у WebSSH: bash webssh-bootstrap.sh
set -euo pipefail

HOME_DIR="/home/ep616268"
APP_DIR="${HOME_DIR}/fortprint.com.ua"
REPO="https://github.com/maksirhPrometey/foruna.git"
DOMAIN="fortprint.com.ua"

find_python() {
    for candidate in /usr/bin/python3.14 /usr/bin/python3.13 /usr/bin/python3.12 \
        /usr/bin/python3.11 /usr/bin/python3.10; do
        if [ -x "${candidate}" ]; then
            echo "${candidate}"
            return 0
        fi
    done
    return 1
}

PYTHON="$(find_python)" || {
    echo "ПОМИЛКА: Python 3.10+ не знайдено."
    echo "Панель → Настройки хостинг-аккаунта → Python 3.12 → Зберегти"
    echo "Потім: source ~/.bashrc && bash webssh-bootstrap.sh"
    exit 1
}

echo "=== FortunaPrint deploy ==="
echo "Python: ${PYTHON} ($(${PYTHON} --version))"

cd "${HOME_DIR}"

if [ ! -d "${APP_DIR}/.git" ]; then
    git clone "${REPO}" "${APP_DIR}"
fi

cd "${APP_DIR}"
git pull origin main

if [ ! -f .env ]; then
    echo ""
    echo "Створення .env — потрібні дані MySQL з панелі (MySQL → Базы данных)"
    read -r -p "DB_NAME [ep616268_fortuna]: " DB_NAME
    DB_NAME="${DB_NAME:-ep616268_fortuna}"
    read -r -p "DB_USER [ep616268_fortuna]: " DB_USER
    DB_USER="${DB_USER:-ep616268_fortuna}"
    read -r -s -p "DB_PASSWORD: " DB_PASSWORD
    echo ""

    SECRET_KEY="$(${PYTHON} -c 'import secrets; print(secrets.token_urlsafe(50))')"

    cat > .env <<EOF
DJANGO_SETTINGS_MODULE=config.settings.production
SECRET_KEY=${SECRET_KEY}
ALLOWED_HOSTS=${DOMAIN},www.${DOMAIN}
CSRF_TRUSTED_ORIGINS=https://${DOMAIN},https://www.${DOMAIN}
SECURE_SSL_REDIRECT=False

DB_ENGINE=mysql
DB_NAME=${DB_NAME}
DB_USER=${DB_USER}
DB_PASSWORD=${DB_PASSWORD}
DB_HOST=127.0.0.1
DB_PORT=3306

TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
EOF
    echo ".env створено"
else
    echo ".env вже існує — пропускаємо"
fi

if [ ! -d .venv ]; then
    "${PYTHON}" -m venv .venv
fi

VENV_PY="${APP_DIR}/.venv/bin/python"

"${VENV_PY}" -m pip install --upgrade pip
"${VENV_PY}" -m pip install -r requirements.txt

export DJANGO_SETTINGS_MODULE=config.settings.production
"${VENV_PY}" manage.py migrate --noinput
"${VENV_PY}" manage.py collectstatic --noinput

if ! "${VENV_PY}" manage.py shell -c "from django.contrib.auth import get_user_model; exit(0 if get_user_model().objects.filter(is_superuser=True).exists() else 1)" 2>/dev/null; then
    echo ""
    echo "Створіть адміністратора:"
    "${VENV_PY}" manage.py createsuperuser
fi

echo ""
echo "=== Готово (код + БД + static) ==="
echo ""
echo "Далі в ПАНЕЛІ ADM.TOOLS:"
echo "1. Сайты → Настройки сайта → ${DOMAIN}"
echo "2. Веб-сервер → Проксирование трафика → Зберегти"
echo "3. Настройки веб-приложения:"
echo "   Каталог: ${APP_DIR}"
echo "   Команда (підстав IP:PORT з панелі замість 127.0.0.1:3000):"
echo "   cd ${APP_DIR} && .venv/bin/gunicorn config.wsgi:application --bind 127.0.0.1:3000 --workers 2 --timeout 120"
echo ""
echo "4. Зберегти → Запустить → перевірити Логи приложения"
echo "5. Сайт: https://${DOMAIN}/"
