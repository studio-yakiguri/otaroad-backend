from .base import *

ALLOWED_HOSTS = []

# Debug Options
DEBUG = False

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
    }
}

# 허용할 Origin 추가
CORS_ALLOWED_ORIGINS = [
    ''
]