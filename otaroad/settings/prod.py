from .base import *
from .util import get_secure_data

ALLOWED_HOSTS = ["127.0.0.1", "api.otaroad.party", "https://map.otaroad.party"]

# Debug Options
DEBUG = False

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
db_data = get_secure_data(".secure/db.json")

if db_data["default"] == "":
    raise ImproperlyConfigured(
        "Please input db.json in .secure/")

DATABASES = db_data

# Application definition
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
}

# 허용할 Origin 추가
CORS_ALLOWED_ORIGINS = [
    "https://subculture-map-frontend.pages.dev",
    "https://map.otaroad.party",
    "http://127.0.0.1:8000",
    "https://api.otaroad.party"
]

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# 신뢰할 수 있는 ORIGIN 추가
CSRF_TRUSTED_ORIGINS = [
    "https://api.otaroad.party", "https://map.otaroad.party"]
