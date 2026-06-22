import os

from config.pymysql_bootstrap import install_pymysql

install_pymysql()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
