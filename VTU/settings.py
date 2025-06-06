"""
Django settings for VTU project.

Generated by 'django-admin startproject' using Django 4.2.13.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

# import os
from pathlib import Path

import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Where collected static files will be stored (for production)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# URL prefix for static files
STATIC_URL = '/static/'

# Where Django should look for static files *in development*
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'Dashboard', 'static'),
    os.path.join(BASE_DIR, 'authentication', 'static'),
]


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*', 'bigsheriffdata.onrender.com']

CSRF_TRUSTED_ORIGINS = [
    'https://bigsheriffdata.onrender.com'
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Dashboard',
    'api',
    'authentication',
    "crispy_forms",
    "crispy_bootstrap4",
    'rest_framework',
    'rest_framework.authtoken',
    'django.contrib.humanize',
    "webhook",

    'drf_yasg',
    'hijack',
    'hijack.contrib.admin',
    'axes',
]

LOGIN_REDIRECT_URL = '/index'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'fake_login_attempts.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
}


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'axes.middleware.AxesMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'hijack.middleware.HijackUserMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesBackend',
    'django.contrib.auth.backends.ModelBackend',
]

AXES_FAILURE_LIMIT = 5  # Lock out after 5 failures
AXES_COOLOFF_TIME = 1  # Lock lasts 1 hour
AXES_LOCK_OUT_AT_FAILURE = True  # Example setting
# AXES_LOCKOUT_CALLABLE = 'your_project.your_app.utils.custom_lockout_response'

ROOT_URLCONF = 'VTU.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'Dashboard.context_processors.account_details',
            ],
        },
    },
]

WSGI_APPLICATION = 'VTU.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = 'Dashboard.CustomUser'

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ]
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
   'rest_framework.permissions.AllowAny',
]}


CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# 5 minutes = 300 seconds
SESSION_COOKIE_AGE = 300  # Time in seconds
SESSION_SAVE_EVERY_REQUEST = True

LOGIN_URL = 'login'

MONNIFY_BASE_URL = os.getenv('MONNIFY_BASE_URL', 'https://api.monnify.com')  # Default to sandbox URL if not found
MONNIFY_AUTH_TOKEN = os.getenv('MONNIFY_AUTH_TOKEN')  

# Signals.py 
MONNIFY_CLIENT_ID = os.getenv("MONNIFY_CLIENT_ID")
MONNIFY_CLIENT_SECRET = os.getenv("MONNIFY_CLIENT_SECRET")
MONNIFY_AUTH_URL = "https://api.monnify.com/api/v1/auth/login"
MONNIFY_BASE_URL = "https://api.monnify.com"
MONNIFY_CONTRACT_CODE = os.getenv("MONNIFY_CONTRACT_CODE")
MONNIFY_RESERVED_ACCOUNTS_URL = "https://api.monnify.com/api/v2/bank-transfer/reserved-accounts"

# APIViews
VTPASS_AUTH_TOKEN = os.getenv("VTPASS_AUTH_TOKEN")
VTPASS_SECRET_KEY = os.getenv("VTPASS_SECRET_KEY")

PAYSTACK_PUBLIC_KEY = os.getenv("PAYSTACK_PUBLIC_KEY")
PAYSTACK_SECRET_KEY = os.getenv("PAYSTACK_SECRET_KEY")

# RestAPI
VTPASS_BASE_URL = os.getenv("VTPASS_BASE_URL", "https://sandbox.vtpass.com")
VTPASS_EMAIL = os.getenv("VTPASS_EMAIL")
VTPASS_PASSWORD = os.getenv("VTPASS_PASSWORD")


MIN_REFERRAL_TRANSFER_AMOUNT = 50.00  # or Decimal('50.00') if you're working with Decimals

EMAIL_BACKEND = os.getenv('EMAIL_BACKEND')
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS") == "True"
EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL") == "True"
EMAIL_PORT = int(os.getenv("EMAIL_PORT"))
# EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')