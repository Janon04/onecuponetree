import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Add apps directory to Python path
sys.path.insert(0, str(BASE_DIR / 'apps'))

# Load environment variables from .env at project root (if present)
load_dotenv(BASE_DIR / '.env')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', os.getenv('DJANGO_SECRET_KEY', 'django-insecure-onecup-one-tree-secret-key-change-in-production'))

# SECURITY WARNING: don't run with debug turned on in production!
DJANGO_DEBUG = os.getenv('DEBUG', os.getenv('DJANGO_DEBUG', 'False'))
DEBUG = str(DJANGO_DEBUG).lower() in ('1', 'true', 'yes')

# Allowed hosts can be a comma-separated list in the env var
ALLOWED_HOSTS = [h.strip() for h in os.getenv('ALLOWED_HOSTS', os.getenv('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1,0.0.0.0')).split(',') if h.strip()]

# CSRF Settings - Fix for production CSRF verification errors
CSRF_TRUSTED_ORIGINS = [o.strip() for o in os.getenv('CSRF_TRUSTED_ORIGINS', 'http://localhost:8000,http://127.0.0.1:8000,http://159.198.68.63:81').split(',') if o.strip()]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',
    # Third-party apps
    'rest_framework',
    'rest_framework.authtoken',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'crispy_forms',
    'crispy_bootstrap5',
    'whitenoise.runserver_nostatic',
    # Local apps
    'accounts',
    'dashboard',
    'gallery',
    'volunteers',
    'core',
    'partners',
    'programs',
    'shop',
    'events',
    'contact',
    'api',
    'blog',
    'farmers',
    'newsletter',
    'get_involved',
    'apps.trees',
    'researchhub',
    'ckeditor',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'onecup_one_tree_website.urls'

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
                'core.context_processors.site_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'onecup_one_tree_website.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# If running in production (set DJANGO_PRODUCTION=True in .env), use MySQL by default.
# You can change `DJANGO_DB` to `postgres` to use the commented Postgres config below.
if os.getenv('DJANGO_PRODUCTION', 'False').lower() in ('1', 'true', 'yes'):
    DB_ENGINE = os.getenv('DJANGO_DB', 'mysql').lower()
    if DB_ENGINE == 'mysql':
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': os.getenv('MYSQL_DATABASE', os.getenv('POSTGRES_DB')),
                'USER': os.getenv('MYSQL_USER', os.getenv('POSTGRES_USER')),
                'PASSWORD': os.getenv('MYSQL_PASSWORD', os.getenv('POSTGRES_PASSWORD')),
                'HOST': os.getenv('MYSQL_HOST', os.getenv('POSTGRES_HOST', 'localhost')),
                'PORT': os.getenv('MYSQL_PORT', '3306'),
            }
        }

# Postgres configuration (kept for reference). To use Postgres, set `DJANGO_DB=postgres`.
# if os.getenv('DJANGO_PRODUCTION', 'False').lower() in ('1', 'true', 'yes') and os.getenv('DJANGO_DB','postgres') == 'postgres':
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.postgresql',
#             'NAME': os.getenv('POSTGRES_DB'),
#             'USER': os.getenv('POSTGRES_USER'),
#             'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
#             'HOST': os.getenv('POSTGRES_HOST', 'localhost'),
#             'PORT': os.getenv('POSTGRES_PORT', '5432'),
#         }
#     }

# Password validation
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
LANGUAGE_CODE = 'en'


TIME_ZONE = 'Africa/Maputo' 

USE_I18N = False

USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model
AUTH_USER_MODEL = 'accounts.User'

# Django Allauth Configuration
SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_UNIQUE_EMAIL = True

# Crispy Forms Configuration
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Django REST Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
}

# Email Configuration (read from environment)
# Use console backend in development if no email credentials provided
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')

if EMAIL_HOST_USER and EMAIL_HOST_PASSWORD:
    EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
    EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
    EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
    EMAIL_USE_TLS = str(os.getenv('EMAIL_USE_TLS', 'True')).lower() in ('1', 'true', 'yes')
    DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER)
else:
    # Development mode - print emails to console
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'noreply@onecupinitiative.org')

CONTACT_NOTIFICATION_EMAIL = os.getenv('CONTACT_NOTIFICATION_EMAIL', 'info@onecupinitiative.org')

# Security Settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# CORS Settings (if needed for API)
CORS_ALLOW_ALL_ORIGINS = os.getenv('CORS_ALLOW_ALL_ORIGINS', 'False').lower() in ('true', '1', 'yes')
CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', 'http://localhost:3000,http://127.0.0.1:3000').split(',')

# Logging Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'django.log',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
}

# Custom Settings for One Cup Initiative
SITE_NAME = os.getenv('SITE_NAME', 'One Cup Initiative')
SITE_DESCRIPTION = os.getenv('SITE_DESCRIPTION', 'A sustainable movement empowering farmers, training youth, and restoring our planet — One Cup at a Time.')
CONTACT_EMAIL = os.getenv('CONTACT_EMAIL', CONTACT_NOTIFICATION_EMAIL)

# Social Media Links
SOCIAL_MEDIA_LINKS = {
    'facebook': os.getenv('SOCIAL_FACEBOOK', 'https://www.facebook.com/share/r/1Cn4fDMwRs/?mibextid=wwXIfr'),
    'twitter': os.getenv('SOCIAL_TWITTER', 'https://x.com/onecuprwanda?s=21'),
    'instagram': os.getenv('SOCIAL_INSTAGRAM', 'https://www.instagram.com/onecuproasters?igsh=MWRqaG0yY3Z0OGU5eQ=='),
    'youtube': os.getenv('SOCIAL_YOUTUBE', 'https://youtu.be/DindpiHNdAA?si=XrxBs5FYDcfUWuzQ'),
}

# Contact Information
CONTACT_PHONE = os.getenv('CONTACT_PHONE', '+250 788 354 403')
CONTACT_ADDRESS = os.getenv('CONTACT_ADDRESS', '16 KG 599 Street, Kigali')
CONTACT_MAP_URL = os.getenv('CONTACT_MAP_URL', 'https://www.google.com/maps/place/One+Cup+Coffeehouse/@-1.9553987,30.1025397,16.81z/data=!4m6!3m5!1s0x19dca7d7008f0575:0x57abf3f2b852188d!8m2!3d-1.9554701!4d30.1026171!16s%2Fg%2F11s4tf7gkg?entry=ttu&g_ep=EgoyMDI1MDgyNS4wIKXMDSoASAFQAw%3D%3D')

# Payment Gateway Settings
PAYMENT_GATEWAYS = {
    'MTN_MOBILE_MONEY': {
        'enabled': os.getenv('MTN_ENABLED', 'False').lower() in ('true', '1', 'yes'),
        'api_key': os.getenv('MTN_API_KEY', ''),
        'secret_key': os.getenv('MTN_SECRET_KEY', ''),
    },
    'RWANDA_PAY': {
        'enabled': os.getenv('RWANDA_PAY_ENABLED', 'False').lower() in ('true', '1', 'yes'),
        'api_key': os.getenv('RWANDA_PAY_API_KEY', ''),
        'secret_key': os.getenv('RWANDA_PAY_SECRET_KEY', ''),
    },
    'PAYPAL': {
        'enabled': os.getenv('PAYPAL_ENABLED', 'False').lower() in ('true', '1', 'yes'),
        'client_id': os.getenv('PAYPAL_CLIENT_ID', ''),
        'client_secret': os.getenv('PAYPAL_CLIENT_SECRET', ''),
        'sandbox': os.getenv('PAYPAL_SANDBOX', 'True').lower() in ('true', '1', 'yes'),
    },
}

# Newsletter Integration (Mailchimp)
MAILCHIMP_API_KEY = os.getenv('MAILCHIMP_API_KEY', '')
MAILCHIMP_LIST_ID = os.getenv('MAILCHIMP_LIST_ID', '')

# Security Settings for Production
# Note: These are set to False for HTTP connections. Change to True when using HTTPS.
SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'False').lower() in ('true', '1', 'yes')
CSRF_COOKIE_SECURE = os.getenv('CSRF_COOKIE_SECURE', 'False').lower() in ('true', '1', 'yes')
CSRF_COOKIE_HTTPONLY = False  # Must be False for AJAX requests to work
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'

# File Upload Settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
