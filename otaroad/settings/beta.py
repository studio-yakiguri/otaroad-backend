from .base import *
from .util import get_secure_data

ALLOWED_HOSTS = ["127.0.0.1", "100.107.194.104",
                 "sc0-nas.wahoo-in.ts.net:8443"]

# Debug Options
DEBUG = False

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
db_data = get_secure_data('.secure/db-beta.json')

if db_data['default'] == "":
    raise ImproperlyConfigured(
        "Please input db-beta.json in .secure/")

DATABASES = db_data

# Application definition
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ]
}

# 허용할 Origin 추가
CORS_ALLOWED_ORIGINS = [
    'https://dev.subculture-map-frontend.pages.dev',
    'http://127.0.0.1:8000',
    'http://100.107.194.104:9500',
    'https://beta.otaroad.party'
    'https://sc0-nas.wahoo-in.ts.net:8443'
]