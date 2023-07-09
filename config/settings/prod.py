from .base import *
from .util import get_key_data

ALLOWED_HOSTS = []

# Debug Options
DEBUG = False


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
secret_key_data = get_key_data('.secure/db.json')


DATABASE = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        'OPTIONS': {
                'init_command': 'SET sql_mode="STRICT_TRANS_TABLES"'
        }
    }
}

# 허용할 Origin 추가
CORS_ALLOWED_ORIGINS = [
    ''
]
