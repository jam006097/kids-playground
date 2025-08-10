from .base import *
import os
import dj_database_url

DEBUG = False
ALLOWED_HOSTS = ["kidsplayground.onrender.com"]

DATABASES = {"default": dj_database_url.config(default=os.getenv("DATABASE_URL"))}

# Email settings for production
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
