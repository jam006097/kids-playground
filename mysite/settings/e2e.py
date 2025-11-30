import os
from pathlib import Path
from .base import *  # Keep this to inherit other settings

# Redefine BASE_DIR locally to avoid flake8 F405 and mypy path issues
# This calculates the path from this settings file itself
BASE_DIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# Static files for E2E tests
# Ensure static files are collected and served during tests
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

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
