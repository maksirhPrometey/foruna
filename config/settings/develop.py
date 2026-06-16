from decouple import config
from .base import *  # noqa: F401, F403

DEBUG = True

SECRET_KEY = config('SECRET_KEY', default='dev-only-insecure-key-do-not-use-in-prod')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # noqa: F405
    }
}

INTERNAL_IPS = ['127.0.0.1']
