#!/bin/bash
# Скрипт деплою на сервері ADM.TOOLS — завантажити в /home/<CPANEL_USER>/deploy_setup.sh
# Запуск: bash deploy_setup.sh  або через Cron у панелі

set -e

CPANEL_USER="ep616268"
HOME_DIR="/home/${CPANEL_USER}"
APPDIR="${HOME_DIR}/backend"
LOG="${HOME_DIR}/deploy_setup.log"
PYTHON_VERSION="3.12"
VENV_PYTHON="${HOME_DIR}/virtualenv/backend/${PYTHON_VERSION}/bin/python"

echo "=== DEPLOY $(date) ===" > "${LOG}"
cd "${APPDIR}"

echo "--- pip install ---" >> "${LOG}"
"${VENV_PYTHON}" -m pip install -r requirements.txt >> "${LOG}" 2>&1

echo "--- migrate ---" >> "${LOG}"
"${VENV_PYTHON}" manage.py migrate --noinput >> "${LOG}" 2>&1

echo "--- collectstatic ---" >> "${LOG}"
"${VENV_PYTHON}" manage.py collectstatic --noinput --clear >> "${LOG}" 2>&1

echo "--- restart passenger ---" >> "${LOG}"
touch "${APPDIR}/passenger_wsgi.py" >> "${LOG}" 2>&1

echo "=== DONE ===" >> "${LOG}"
