# antiGPTproject/settings.py
from pathlib import Path
import os

# BASE_DIR
BASE_DIR = Path(__file__).resolve().parent.parent

# -----------------------
# SECURITY / environment
# -----------------------
# Read secret key from env (fall back to a dev value only)
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")

# Robust DEBUG parsing
def _bool_env(name, default=False):
    val = os.environ.get(name)
    if val is None:
        return default
    return str(val).lower() in ("1", "true", "yes", "on")

DEBUG = _bool_env("DEBUG", True)

# ALLOWED_HOSTS: comma-separated in env, otherwise sensible defaults
_raw_allowed = os.environ.get("ALLOWED_HOSTS", "").strip()
if _raw_allowed:
    ALLOWED_HOSTS = [h.strip() for h in _raw_allowed.split(",") if h.strip()]
else:
    # Development defaults; in production set ALLOWED_HOSTS env var explicitly
    ALLOWED_HOSTS = ["localhost", "127.0.0.1"] if DEBUG else []

# CSRF trusted origins (comma-separated), useful when running behind HTTPS proxies
_raw_csrf = os.environ.get("CSRF_TRUSTED_ORIGINS", "").strip()
if _raw_csrf:
    CSRF_TRUSTED_ORIGINS = [u.strip() for u in _raw_csrf.split(",") if u.strip()]
else:
    CSRF_TRUSTED_ORIGINS = []

# When behind a proxy (like Render), trust X-Forwarded-Proto for scheme
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# -----------------------
# Applications
# -----------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "chatbot",
    "accounts",
]

# Middleware (Whitenoise near the top)
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",   # serves static files in production
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "antiGPTproject.urls"

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
            ],
        },
    },
]

WSGI_APPLICATION = "antiGPTproject.wsgi.application"

# -----------------------
# Database (default: SQLite)
# -----------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# -----------------------
# Auth, Internationalization
# -----------------------
AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = False

# -----------------------
# Static files (collectstatic target)
# -----------------------
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [BASE_DIR / "static"]

# Use Whitenoise compressed manifest storage in production for better caching
if not DEBUG:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# -----------------------
# Defaults and login redirects
# -----------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "conversations"
LOGOUT_REDIRECT_URL = "login"
