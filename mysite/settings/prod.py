from .base import *
import os
import dj_database_url

DEBUG = False
ALLOWED_HOSTS = ["kidsplayground.onrender.com"]

# Security settings for production
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
# HSTS settings (start with a small value for safety)
# Read more: https://docs.djangoproject.com/en/5.0/ref/settings/#secure-hsts-seconds
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

DATABASES = {"default": dj_database_url.config(default=os.getenv("DATABASE_URL"))}

# Email settings for production
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")

# AI Summary API Settings for Production
AI_SUMMARY_API_URL = os.getenv("AI_SUMMARY_API_URL")
AI_SUMMARY_API_KEY = os.getenv("AI_SUMMARY_API_KEY")
AI_SUMMARY_API_USERNAME = os.getenv("AI_SUMMARY_API_USERNAME")
AI_SUMMARY_API_TIMEOUT = int(os.getenv("AI_SUMMARY_API_TIMEOUT", 60))
