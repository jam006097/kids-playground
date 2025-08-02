from .base import *
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

# Email settings for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
