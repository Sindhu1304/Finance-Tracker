from datetime import timedelta
from pathlib import Path
from decouple import config
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

ALLOWED_HOSTS = config("ALLOWED_HOSTS").split(" ")


# Application definition
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "drf_spectacular",
    "corsheaders",
    "rest_framework_simplejwt.token_blacklist",
    # "debug_toolbar"
]

LOCAL_APPS = [
    "apps.accounts",
    "apps.expenses",
    "apps.user_stats",
    "apps.social_accounts",
    'apps.common'
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "Expenses_API.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "Expenses_API.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

AUTH_USER_MODEL = "accounts.user"

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "NON_FIELD_ERROR_KEYS": "error",
    "EXCEPTION_HANDLER": "utils.exception_handler.custom_exception_handler",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config("EMAIL_HOST")
EMAIL_PORT = config("EMAIL_PORT")
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
EMAIL_USE_SSL = config("EMAIL_USE_SSL")
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL")


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = "/static/"
MEDIA_URL = "/media/"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static/"),
]
MEDIA_ROOT = os.path.join(BASE_DIR, "static/media")
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(minutes=7),
}

CORS_ORIGIN_ALLOW_ALL = True

GOOGLE_CLIENT_ID = config("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = config("GOOGLE_CLIENT_SECRET")
SOCIAL_AUTH_PASSWORD = config("SOCIAL_AUTH_PASSWORD")


SPECTACULAR_SETTINGS = {
    "TITLE": "Expense API",
    "DESCRIPTION": """
    An expense tracker API built with django rest framework. 
    For testing using existing account, login with the following credentials:

    email: steppaapitestuser@gmail.com
    password: testuser
    or 
    create your own account :)
    """,
    "VERSION": "1.0.0",
    "SECURITY": [
        {
            "bearerAuth": [],
        }
    ],
    "TAGS": [
        {"name": "Auth", "description": "Authentication Endpoints"},
        {"name": "Social Auth", "description": "Social Authentication Endpoints"},
        {"name": "Account Settings", "description": "User Account operations"},
        {"name": "Expenses", "description": "Expenses CRUD endpoints"},
        {"name": "Category", "description": "Category CRUD endpoints"},
        {"name": "Stats", "description": "User Stats"},
    ],
}
