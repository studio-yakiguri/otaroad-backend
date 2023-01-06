from .base import *

ALLOWED_HOSTS = []

# Debug Options
DEBUG = True

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}

# 허용할 Origin 추가
CORS_ORIGIN_ALLOW_ALL = True
