from .base import *

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# Use a separate database for E2E tests if desired, or rely on pytest-django's test DB creation
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": "e2e_test_db",
#         "USER": "e2e_user",
#         "PASSWORD": "e2e_password",
#         "HOST": "localhost",
#         "PORT": "5432",
#     }
# }

# Static files for E2E tests
# Ensure static files are collected and served during tests
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

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
