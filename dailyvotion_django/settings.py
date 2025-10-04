
from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env if present (for local development)
load_dotenv(BASE_DIR / '.env')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY: Use environment variables in production
SECRET_KEY = os.getenv('SECRET_KEY', '0dd396c54ec088e33b0be54f297fabb5')

# DEBUG from env; default True for local dev
DEBUG = os.getenv('DEBUG', 'True').lower() in ('1', 'true', 'yes')

# Configure allowed hosts; derive from Render external URL when present
ALLOWED_HOSTS = []
render_external_url = os.getenv('RENDER_EXTERNAL_URL')
if render_external_url:
    # RENDER_EXTERNAL_URL looks like https://your-app.onrender.com
    try:
        from urllib.parse import urlparse
        parsed = urlparse(render_external_url)
        if parsed.hostname:
            ALLOWED_HOSTS.append(parsed.hostname)
    except Exception:
        pass

# Allow explicit comma-separated list via env
env_allowed = os.getenv('ALLOWED_HOSTS')
if env_allowed:
    ALLOWED_HOSTS.extend([h.strip() for h in env_allowed.split(',') if h.strip()])


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'dailyvotion_django.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'dailyvotion_django.context_processors.static_version',
            ],
        },
    },
]

WSGI_APPLICATION = 'dailyvotion_django.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# Detect Render environment; use INTERNAL_DATABASE_URL only on Render.
_on_render = bool(os.getenv('RENDER') or os.getenv('RENDER_SERVICE_ID') or os.getenv('RENDER_EXTERNAL_URL'))
_internal = os.getenv('INTERNAL_DATABASE_URL')
_primary = os.getenv('DATABASE_URL')
_external = os.getenv('EXTERNAL_DATABASE_URL')

# Always prefer explicit DATABASE_URL if provided (for both Render and local)
if _primary:
    # Set SSL requirement based on the URL (require SSL for render.com domains)
    _require_ssl = 'render.com' in _primary
    DATABASES = {'default': dj_database_url.parse(_primary, conn_max_age=600, ssl_require=_require_ssl)}
elif _on_render and _internal:
    # On Render with internal DB URL
    DATABASES = {'default': dj_database_url.parse(_internal, conn_max_age=600, ssl_require=True)}
elif _external:
    # External DB URL as last resort for explicit DB connections
    DATABASES = {'default': dj_database_url.parse(_external, conn_max_age=600, ssl_require=True)}
else:
    # Fallback to SQLite if no database URL is provided
    DATABASES = {'default': dj_database_url.config(default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}", conn_max_age=600)}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

# Always include leading and trailing slashes for STATIC_URL
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
# Optionally expose React public assets (favicon.ico, logos) if present locally
_react_public = BASE_DIR / 'DailyVotion-App' / 'public'
if _react_public.exists():
    STATICFILES_DIRS.append(_react_public)
STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise storage: use CompressedManifestStaticFilesStorage for better caching
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Version string for cache busting (can override via STATIC_VERSION env var)
STATIC_VERSION = os.getenv('STATIC_VERSION', '2025-10-04')

# CSRF trusted origins: include Render external URL
CSRF_TRUSTED_ORIGINS = []
if render_external_url:
    try:
        from urllib.parse import urlparse as _urlparse
        _p = _urlparse(render_external_url)
        if _p.scheme and _p.netloc:
            CSRF_TRUSTED_ORIGINS.append(f"{_p.scheme}://{_p.netloc}")
    except Exception:
        pass
extra_csrf = os.getenv('CSRF_TRUSTED_ORIGINS')
if extra_csrf:
    CSRF_TRUSTED_ORIGINS.extend([o.strip() for o in extra_csrf.split(',') if o.strip()])

# Security headers when not in debug
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    X_FRAME_OPTIONS = 'DENY'

# Auth redirects (used by Django login/logout flows when enabled)
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/login/'

# Session settings: keep users logged in across browser restarts
# 30 days by default; can be overridden via env SESSION_COOKIE_AGE (seconds)
SESSION_COOKIE_AGE = int(os.getenv('SESSION_COOKIE_AGE', str(60 * 60 * 24 * 30)))
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
# Refresh the session expiry on each request to maintain activity-based persistence
SESSION_SAVE_EVERY_REQUEST = True

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Media files (user uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
os.makedirs(MEDIA_ROOT, exist_ok=True)
WHITENOISE_MAX_AGE = 31536000  # 1 year for static

# Admin pre-auth configuration (single permanent code)
# For best security, override via environment variable ADMIN_AUTH_CODE in production.
ADMIN_AUTH_CODE = os.getenv('ADMIN_AUTH_CODE', 'DV-Admin').strip()