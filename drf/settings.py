from pathlib import Path
import os
from datetime import timedelta
from typing import List
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-(ma!0=%dn(gqh@a0q*1x5-09sp&0e^+9pwidt%+0#7aat)jrjj"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["vercel.app", "*"]
CORS_ALLOWED_ORIGINS: List[str] = []

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",


    # LOCAL_APPS
    "solutions",


    # THIRD_PARTY_LIBRARIES
    "rest_framework",
    "rest_framework_swagger",
    "rest_framework_simplejwt",
    "drf_yasg",
    "corsheaders",
    # "rest_framework_simplejwt.token_blacklist",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# Session settings

SESSION_ENGINE = "django.contrib.sessions.backends.db"
SESSION_COOKIE_NAME = "sessionid"
SESSION_COOKIE_AGE = 1209600
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = True
SESSION_SAVE_EVERY_REQUEST = False
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# Set the session timeout to one year (in seconds)
# 1 year = 365 days * 24 hours * 60 minutes * 60 seconds
SESSION_COOKIE_AGE = 365 * 24 * 60 * 60


ROOT_URLCONF = "drf.urls"

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

WSGI_APPLICATION = "drf.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "railway",
        "USER": "postgres",
        "PASSWORD": "*2FAg3BdFa-CDaD*df32eFcB3Fg4AEGa",
        "HOST": "viaduct.proxy.rlwy.net",
        "PORT": "55835",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Africa/Nairobi"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles_build", "static")
STATIC_URL = "/staticfiles/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "")]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:8000",
    "http://localhost:5173",
    "https://unity-solutions.vercel.app",
    "https://www.unitysolutionstutors.com",
]


REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.MultiPartParser",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 15,
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
}


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=14),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": False,
}

AUTH_USER_MODEL = "solutions.User"

SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"}
    }
}

# # Mail server
# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST = (
#     os.environ["EMAIL_HOST"] if "EMAIL_HOST" in os.environ else config("EMAIL_HOST")
# )
# EMAIL_PORT = (
#     os.environ["EMAIL_PORT"] if "EMAIL_PORT" in os.environ else config("EMAIL_PORT")
# )
# EMAIL_HOST_USER = (
#     os.environ["EMAIL_HOST_USER"]
#     if "EMAIL_HOST_USER" in os.environ
#     else config("EMAIL_HOST_USER")
# )
# EMAIL_HOST_PASSWORD = (
#     os.environ["EMAIL_HOST_PASSWOR    D"]
#     if "EMAIL_HOST_PASSWORD" in os.environ
#     else config("EMAIL_HOST_PASSWORD")
# )
# EMAIL_USE_TLS = (
#     os.environ["EMAIL_USE_TLS"]
#     if "EMAIL_USE_TLS" in os.environ
#     else config("EMAIL_USE_TLS")
# )
# EMAIL_USE_SSL = (
#     os.environ["EMAIL_USE_SSL"]
#     if "EMAIL_USE_SSL" in os.environ
#     else config("EMAIL_USE_SSL")
# )
# DEFAULT_FROM_EMAIL = (
#     os.environ["DEFAULT_FROM_EMAIL"]
#     if "DEFAULT_FROM_EMAIL" in os.environ
#     else config("DEFAULT_FROM_EMAIL")
# )

# # IMAP settings
# IMAP_HOST = config("SMTP_HOST")
# IMAP_USER = config("SMTP_USER")
# # IMAP_USER = "sopacrmtest@gmail.com"
# print(IMAP_USER)
# IMAP_PASSWORD = config("SMTP_PASSWORD")
# # IMAP_PASSWORD = "pibqyafshnzeyxtx"
# IMAP_PORT = config("SMTP_PORT")
# IMAP_USE_TLS = config("SMTP_USE_TLS")
# # pop mail settings
# POP_HOST = config("POP_HOST")
# POP_USER = config("POP_USER")
# POP_PASSWORD = config("POP_PASSWORD")
# POP_PORT = config("POP_PORT")
# POP_USE_TLS = config("POP_USE_TLS")

# # SMS Gateway
# SMS_GATEWAY_API_KEY = (
#     os.environ["SMS_GATEWAY_API_KEY"]
#     if "SMS_GATEWAY_API_KEY" in os.environ
#     else config("SMS_GATEWAY_API_KEY")
# )
# SMS_SENDER_ID = (
#     os.environ["SMS_SENDER_ID"]
#     if "SMS_SENDER_ID" in os.environ
#     else config("SMS_SENDER_ID")
# )
