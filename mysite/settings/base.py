from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url

# BASE_DIRの定義
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# .env 読み込み
load_dotenv(os.path.join(BASE_DIR, ".env"))

SECRET_KEY = os.getenv("SECRET_KEY")

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "csp",
    "myapp",
    "users",
    "bootstrap4",
    "django_crontab",
    "accounts",
    # allauth
    "allauth",
    "allauth.account",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "csp.middleware.CSPMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # allauth middleware
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "mysite.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "myapp.context_processors.site_name",
            ],
        },
    },
]

WSGI_APPLICATION = "mysite.wsgi.application"

DATABASES = {"default": dj_database_url.config(default=os.getenv("DATABASE_URL"))}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# I18N
LANGUAGE_CODE = "ja"
TIME_ZONE = "Asia/Tokyo"
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# WhiteNoiseの設定を追加
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Default primary key
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "users.CustomUser"

# --- allauth 設定 ---
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

SITE_ID = 1
SITE_NAME = "親子で遊ぼうナビ"
LOGIN_REDIRECT_URL = "/"
ACCOUNT_LOGOUT_REDIRECT_URL = "/accounts/login/"

# django-allauth（カスタムユーザーモデル用）設定
ACCOUNT_AUTHENTICATION_METHODS = ["email"]
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_LOGIN_METHODS = {"email"}
ACCOUNT_SIGNUP_FIELDS = ["email*", "password1*", "password2*"]
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True


# ロギング設定
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(asctime)s %(levelname)s %(message)s",
        },
    },
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(BASE_DIR, "app.log"),
            "maxBytes": 1024 * 1024 * 5,  # 5 MB
            "backupCount": 5,
            "formatter": "verbose",
        },
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": True,
        },
        "myapp": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

# cron設定
CRONJOBS = [("0 0 1 * *", "myapp.management.commands.fetch_playgrounds")]


# Content Security Policy (CSP) settings
# https://django-csp.readthedocs.io/en/latest/
CONTENT_SECURITY_POLICY = {
    "DIRECTIVES": {
        "default-src": ("'self'",),
        "script-src": (
            "'self'",
            "ajax.googleapis.com",
            "cdnjs.cloudflare.com",
            "use.fontawesome.com",
            "www.googletagmanager.com",
            "stats.g.doubleclick.net",  # For Google Analytics
            "analytics.google.com",  # For Google Analytics
            "cdn.jsdelivr.net",  # For Bootstrap
            "unpkg.com",  # For Leaflet
            "'sha256-byly89INaW5OlnSUBFJrkf3zS2e/MPPjW507b0aNIzc='",  # For inline script (original)
            "'sha256-bRNsevt2vDj4vEdivjSCVt0GbXKt+Lh/PVAAnkcFW9s='",  # For inline script (accounts/email/)
        ),
        "style-src": (
            "'self'",
            "stackpath.bootstrapcdn.com",
            "cdnjs.cloudflare.com",
            "use.fontawesome.com",
            "fonts.googleapis.com",
            "cdn.jsdelivr.net",  # For Bootstrap
            "unpkg.com",  # For Leaflet
            "'unsafe-inline'",
            # Temporarily allow for development, but should be removed or use nonces/hashes in production
        ),
        "img-src": (
            "'self'",
            "data:",  # Allow data URIs for images (e.g., small icons)
            "www.google.co.jp",  # For Google Maps images/tiles
            "www.gstatic.com",
            "unpkg.com",  # For Leaflet images
            "*.tile.openstreetmap.org",  # For OpenStreetMap tiles
        ),
        "font-src": (
            "'self'",
            "cdnjs.cloudflare.com",
            "use.fontawesome.com",
            "fonts.gstatic.com",
        ),
        "connect-src": (
            "'self'",
            "analytics.google.com",
            "stats.g.doubleclick.net",
            "cdn.jsdelivr.net",  # For Bootstrap source maps
            "unpkg.com",  # For Leaflet source maps
            "stackpath.bootstrapcdn.com",  # For Bootstrap CSS map
        ),
        "frame-src": (
            "'self'",
            "www.google.co.jp",  # For Google Maps iframes
            "maps.google.com",
            "maps.app.goo.gl",
        ),
        "object-src": ("'none'",),  # Disallow <object>, <embed>, <applet>
        "base-uri": ("'self'",),
        "form-action": ("'self'",),
        "frame-ancestors": ("'self'",),
    },
    "REPORT_URI": None,  # Optional: URL to send CSP violation reports to
}
