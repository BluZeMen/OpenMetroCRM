import json
import os
from pathlib import Path


# Utilities
PROJECT_PACKAGE = Path(__file__).resolve().parent.parent

# The full path to the repository root.
BASE_DIR = PROJECT_PACKAGE.parent

data_dir_key = 'METROCRM_DATA_DIR'
DATA_DIR = Path(os.environ[data_dir_key]) if data_dir_key in os.environ else BASE_DIR.parent

try:
    with DATA_DIR.joinpath('conf', 'secrets.json').open() as handle:
        SECRETS = json.load(handle)
except IOError:
    SECRETS = {
        'secret_key': 'a',
        # 'superfeedr_creds': ['any@email.com', 'some_string'],
    }

# django-registration
ACCOUNT_ACTIVATION_DAYS = 3

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators
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

AUTH_USER_MODEL = 'personnel.Contact'

# Django settings
CACHE_MIDDLEWARE_SECONDS = 60 * 3  # 3 minutes
CACHE_MIDDLEWARE_KEY_PREFIX = 'django'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'django_1',
        'USER': 'django_1',
        'HOST': SECRETS.get('db_host', ''),
        'PASSWORD': SECRETS.get('db_password', ''),
    }
}


DEFAULT_FROM_EMAIL = 'testmailingserver@yandex.ru'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_HOST_USER = DEFAULT_FROM_EMAIL
EMAIL_HOST_PASSWORD = SECRETS.get('mail_server_pass', ''),
EMAIL_PORT = 587
EMAIL_USE_TLS = True


# Application definition
FIXTURE_DIRS = [str(PROJECT_PACKAGE.joinpath('fixtures'))]


INSTALLED_APPS = [
    'site_app',
    'personnel',
    'items',
    'messaging',

    'registration',
    'django_cleanup',

    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
]


LANGUAGE_CODE = 'ru-ru'


LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/login/'
LOGOUT_URL = LOGIN_URL


LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "simple": {"format": "[%(name)s] %(levelname)s: %(message)s"},
        "full": {"format": "%(asctime)s [%(name)s] %(levelname)s: %(message)s"},
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[%(server_time)s] %(message)s',
        },
    },
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
    },
    "loggers": {
        "django.request": {
            "handlers": [],
            "level": "ERROR",
            "propagate": False,
        },
        'django.server': {
            'handlers': ['django.server'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}


MEDIA_URL = '/media/'

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# GETTING-STARTED: change 'site_app' to your project name:
ROOT_URLCONF = 'site_app.urls'


SECRET_KEY = str(SECRETS['secret_key'])

SECURE_BROWSER_XSS_FILTER = True

SECURE_CONTENT_TYPE_NOSNIFF = True

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTOCOL", "https")

SERVER_EMAIL = EMAIL_HOST_USER

SESSION_COOKIE_HTTPONLY = True

SILENCED_SYSTEM_CHECKS = [
    'fields.W342',  # tracdb has ForeignKey(unique=True) in lieu of multi-col PKs
    'security.W008',  # SSL redirect is handled by nginx
    'security.W009',  # SECRET_KEY is setup through Ansible secrets
]


SITE_ID = 1


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATICFILES_DIRS = [str(DATA_DIR.joinpath('static_content', 'static'))]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

STATIC_URL = '/static/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(PROJECT_PACKAGE.joinpath('templates'))],
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

TIME_ZONE = 'Europe/Moscow'

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

USE_I18N = True

USE_L10N = True

USE_TZ = True


WSGI_APPLICATION = 'site_app.wsgi.application'
