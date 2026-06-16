"""
Точка входу Passenger (ADM.TOOLS / Ukraine.com.ua — Setup Python App).
Лежить поруч із manage.py, не в public_html.
"""
import os
import sys

from config.pymysql_bootstrap import install_pymysql

install_pymysql()

project_dir = os.path.dirname(os.path.abspath(__file__))
if project_dir not in sys.path:
    sys.path.insert(0, project_dir)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
