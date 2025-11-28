# antiGPTproject/settings.py
from pathlib import Path
import os

# BASE_DIR
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY — use environment variables in production
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here')
DEBUG = os.environ.get('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',') if os.environ.get('ALLOWED_HOSTS') else []

# Applications
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'chatbot',
    'accounts',
]

# Middleware (Whitenoise added near the top)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',   # ← serves static files in production
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'antiGPTproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'antiGPTproject.wsgi.application'

# Database (keep SQLite for now)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True

# NOTE: you previously had USE_TZ = False. Keep False if you prefer naive datetimes.
# If you want timezone-aware datetimes, set USE_TZ = True and ensure your templates / display handle it.
USE_TZ = False

# ----------------------------------------
# STATIC FILE SETTINGS (collectstatic target)
# ----------------------------------------
STATIC_URL = '/static/'

# Use os.path.join to avoid issues on some hosts
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Optional: during development keep your project-level static folder
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Optional whitenoise storage (uncomment if you want compressed manifest storage)
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Login URLs — set to the name used in your urls.py
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = 'conversations'   # <-- matches path(..., name='conversations')
LOGOUT_REDIRECT_URL = 'login'
