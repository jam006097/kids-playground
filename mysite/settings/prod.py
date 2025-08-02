from .base import *
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

# Email settings for production
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
