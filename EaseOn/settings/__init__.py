# -*- coding: utf-8 -*-
import os
import sys
import environ
from .authentication import *
from .celery import *
from .chat import *
from .db import *
from .django_extentions import *
from .email import *
from .gsx import *
from .logging import *
from .rest import *
from .geo_location import *

root = environ.Path(__file__) - 1  # three folder back (/a/b/c/ - 3 = /)
env = environ.Env(DEBUG=(bool, False))  # set default values and casting
environ.Env.read_env()  # reading .env file

ENV = env("ENV", default="PROD")
SMS_BACKEND_KEY = env("SMS_BACKEND_KEY", default="XXXX")
APP_INDIA_USERNAME = env("APP_INDIA_USERNAME", default="XXXX")
APP_INDIA_PASSWORD = env("APP_INDIA_PASSWORD", default="XXXX")
APP_INDIA_SENDER = env("APP_INDIA_SENDER", default="XXXX")
ADMIN_SITE_HEADER = env("ADMIN_SITE_HEADER", default="XXXX")
SITE_HEADER = env("SITE_HEADER", default="XXXX")
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = environ.Path(__file__) - 2
APPS_DIR = os.path.join(BASE_DIR, "apps")
sys.path.insert(0, APPS_DIR)
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY", default="XXXX")
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = not env("DEBUG", default=1, cast=bool)
ALLOWED_HOSTS = env("ALLOWED_HOSTS", default="*")
# Multitenant
ORGANIZATIONS_ORGANIZATION_MODEL = "organizations.Organization"
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
# Application definition
ADMIN_NAME = env("ADMIN_NAME", default="XXXX")
ADMIN_EMAIL = env("ADMIN_EMAIL", default="XXXX")
ADMIN_CONTACT_NUMBER = env("ADMIN_CONTACT_NUMBER", default="XXXX")
ADMINS = [(ADMIN_NAME, ADMIN_EMAIL)]
APPEND_SLASH = False
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
THIRD_PART_PACKAGES = [
    "django_extensions",
    "django_filters",
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
    "oauth2_provider",
]

LOCAL_APPS = [
    "core",
    "otp",
    "customers",
    "devices",
    "inventory",
    "lists",
    "organizations",
    "slas",
    "tickets",
    "tokens",
    "gsx",
    "reporting",
    "rocketchat",
]


INSTALLED_APPS.extend(THIRD_PART_PACKAGES)
INSTALLED_APPS.extend(LOCAL_APPS)


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "oauth2_provider.middleware.OAuth2TokenMiddleware",
]
ROOT_URLCONF = "EaseOn.urls"
TEMPLATES_DIR = os.path.join(BASE_DIR, "EaseOn/", "templates")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
if not os.path.exists(REPORTS_DIR):
    os.mkdir(REPORTS_DIR)

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATES_DIR],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.utils.context_processors.site_defaults",
            ]
        },
    }
]


WSGI_APPLICATION = "EaseOn.wsgi.application"


LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = "/django_static/"
STATICFILES_DIRS = []
STATIC_ROOT = os.path.join(BASE_DIR, "django_static")


CORS_ORIGIN_WHITELIST = [
    "https://easeon.in",
    "https://test.easeon.in",
    "http://localhost:3000",
    "https://localhost:3000",
]
CORS_ALLOW_CREDENTIALS = True

SERVER_IP = env("SERVER_IP", default="XXXX/").strip("/")
CLIENT_URL = env("CLIENT_URL", default="XXXX/").strip("/")
NEW_USER_EMAIL_VERIFICATION_URL = "{}/{}/".format(
    CLIENT_URL, "email_verification"
).strip("/")
NEW_USER_ADMIN_APPROVE_URL = "{}/{}/".format(
    CLIENT_URL, "dashboard/user_approve"
).strip("/")
PASSWORD_RESET_URL = "{}/{}/".format(CLIENT_URL, "password_reset_confirm").strip("/")
CUSTOMER_TICKET_DISPLAY_URL = "{}/{}/".format(CLIENT_URL, "ticket_status").strip("/")

VALID_CLIENT_DOMAIN_NAMES = [
    "uipl.co.in",
    "unicornstore.in",
    "easeon.in",
    "unicorn.com",
]

# GSX

TICKET_SUFFIX = 2
ACCESS_TOKEN_EXPIRE_SECONDS = 60
REFRESH_TOKEN_EXPIRE_SECONDS = 3600
EXEMPTED_DEVICE = ["FCGT24E5HFM2", "ZZ501AAAOWP"]
ENABLE_MULTIPLE_TICKETS_FOR_CUSTOMER = True
REAL_TIME_API_URL=env('REAL_TIME_API_URL',default='https://www.easeon.in:8000/api')