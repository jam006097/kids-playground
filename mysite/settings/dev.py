from .base import *
import os
import sys

DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# AI Summary API Settings
AI_SUMMARY_API_URL = os.getenv(
    "AI_SUMMARY_API_URL", "https://kina006097-kids-playground-ai-api.hf.space/"
)
AI_SUMMARY_API_TIMEOUT = int(os.getenv("AI_SUMMARY_API_TIMEOUT", 30))


# Logging settings for development (override base.py)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(asctime)s %(levelname)s %(module)s %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",  # Show DEBUG level messages in the console
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
        "myapp": {
            "handlers": ["console"],
            "level": "DEBUG",  # Set myapp to DEBUG level
            "propagate": False,
        },
    },
}


# ローカルでの手動テスト時のみ実際にメールを送信する
if "runserver" in sys.argv:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = "smtp.gmail.com"
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
else:
    # テスト実行時はコンソールに出力
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
