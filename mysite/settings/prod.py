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

DEBUG = False
ALLOWED_HOSTS = ["jam006097.pythonanywhere.com"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "jam006097$kids",
        "USER": "jam006097",
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": "jam006097.mysql.pythonanywhere-services.com",
        "PORT": "3306",
    }
}
