import os
from pathlib import Path
from .base import *  # Keep this to inherit other settings

# Redefine BASE_DIR locally to avoid flake8 F405 and mypy path issues
# This calculates the path from this settings file itself
BASE_DIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# Database settings for E2E tests - explicitly set host to localhost
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "kidsplayground_db"),
        "USER": os.getenv("DB_USER", "kina"),
        "PASSWORD": os.getenv("DB_PASSWORD", "Kaim2308!"),
        "HOST": "localhost",  # Explicitly set to localhost for host-based E2E tests
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}

# Static files for E2E tests
# Ensure static files are collected and served during tests
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "myapp", "static", "js", "dist"),
]

# Logging for E2E tests (optional)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
        },
    },
}
