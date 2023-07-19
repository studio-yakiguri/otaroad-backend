from .base import *
from .util import get_secure_data

<<<<<<< HEAD
ALLOWED_HOSTS = ["127.0.0.1", "100.107.194.104"]
=======
ALLOWED_HOSTS = ["127.0.0.1", "api.otaroad.party"]
>>>>>>> 20eabba1b9d3f0f70a3b498c98222418d9e11658

# Debug Options
DEBUG = False

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
db_data = get_secure_data('.secure/db.json')

if db_data['default'] == "":
    raise ImproperlyConfigured(
        "Please input db.json in .secure/")

DATABASES = db_data

# Application definition
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ]
}

# 허용할 Origin 추가
CORS_ALLOWED_ORIGINS = [
    'https://subculture-map-frontend.pages.dev',
    'https://map.otaroad.party',
    'http://127.0.0.1:8000',
<<<<<<< HEAD
=======
    'https://api.otaroad.party'
>>>>>>> 20eabba1b9d3f0f70a3b498c98222418d9e11658
]
