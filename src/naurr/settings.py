"""Django settings for naurr project."""

from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

from decouple import Choices, Csv, config
from dj_database_url import parse as db_url

SRC_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = SRC_DIR.parent

ENVIRONMENT = config(
    "ENVIRONMENT",
    default="local",
    cast=Choices(["local", "production"]),
)

SECRET_KEY = config("SECRET_KEY", default=None)
if not SECRET_KEY:
    if ENVIRONMENT == "local":
        SECRET_KEY = "CHANGE_ME"  # noqa
    else:
        raise ImproperlyConfigured(
            "You need to provide 'SECRET_KEY' when not running in a local environment"
        )


DEBUG = config("DEBUG", default=False, cast=bool)
if DEBUG and ENVIRONMENT != "local":
    raise ImproperlyConfigured(
        "You need to disable 'DEBUG' when not running a local environment"
    )

ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    default=None,
    cast=Csv(),
)

INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    # naurr
    "naurr",
    "filesystem",
    # Third party
    "rest_framework",
    "rest_framework.authtoken",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "naurr.urls"

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

WSGI_APPLICATION = "naurr.wsgi.application"

DATABASES = {
    "default": config(
        "DATABASE_URL",
        default="postgres://postgres@localhost/naurr",
        cast=db_url,
    ),
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
        ),
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

USE_TZ = True
TIME_ZONE = "UTC"

USE_I18N = False

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

LOGIN_URL = "admin:login"
LOGIN_REDIRECT_URL = "admin:index"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Needed for CSRF protection when running behind NGINX and Gunicorn
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

#########################
# Django REST Framework #
#########################
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ),
}
