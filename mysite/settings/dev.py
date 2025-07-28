from .base import (
    BASE_DIR,
    SECRET_KEY,
    INSTALLED_APPS,
    MIDDLEWARE,
    ROOT_URLCONF,
    TEMPLATES,
    WSGI_APPLICATION,
    AUTH_PASSWORD_VALIDATORS,
    LANGUAGE_CODE,
    TIME_ZONE,
    USE_I18N,
    USE_TZ,
    STATIC_URL,
    STATIC_ROOT,
    DEFAULT_AUTO_FIELD,
    CRONJOBS,
)
import os

DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "mydatabase",
        "USER": "myuser",
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": "localhost",
        "PORT": "3306",
    }
}
