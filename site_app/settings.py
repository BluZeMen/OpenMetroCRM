"""
Django settings for myproject project.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys

from django.utils.translation import ugettext_lazy as _

# # Fix relative import of 3.x pyton's 
# # http://stackoverflow.com/questions/16981921/relative-imports-in-python-3
# PACKAGE_PARENT = '..'
# SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
# sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))


ON_PRODUCTION = 'IS_PRODUCTION' in os.environ

if ON_PRODUCTION:
    SECRET_KEY = os.environ['OPENSHIFT_SECRET_TOKEN']

    #todo: fix this!!!
    # dirty dirty dirty hack
    SECRET_KEY = ')_7av^!cy(wfx=k#3*7x+(=j^fzv+ot^1@sh9s9t=8$bu@r(z$'
else:
    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = ')_7av^!cy(wfx=k#3*7x+(=j^fzv+ot^1@sh9s9t=8$bu@r(z$'

# SECURITY WARNING: don't run with debug turned on in production!
# adjust to turn off when on Openshift, but allow an environment variable to override on PAAS
DEBUG = not ON_PRODUCTION
DEBUG = DEBUG or os.getenv("debug","false").lower() == "true"

DEBUG = True

ALLOWED_HOSTS = ['109.234.37.121']
if not ON_PRODUCTION and DEBUG:
    print("*** Warning - Debug mode is on ***")

if ON_PRODUCTION:
    from socket import gethostname
    ALLOWED_HOSTS = [gethostname(),'109.234.37.121']


DJ_PROJECT_DIR = os.path.dirname(__file__)
BASE_DIR = DJ_PROJECT_DIR
WSGI_DIR = os.path.dirname(BASE_DIR)
REPO_DIR = os.path.dirname(WSGI_DIR)
DATA_DIR = os.environ.get('OPENSHIFT_DATA_DIR', BASE_DIR)

# sys.path.append(os.path.join(REPO_DIR, 'libs'))
# import secrets
# SECRETS = secrets.getter(os.path.join(DATA_DIR, 'secrets.json'))

# # Quick-start development settings - unsuitable for production
# # See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# # SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = SECRETS['secret_key']

LOGIN_REDIRECT_URL = '/admin/'
LOGIN_URL = '/admin/login/'
LOGOUT_URL = LOGIN_URL

# ADMIN_MEDIA_PREFIX = '/static/admin/'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_HOST_USER = 'some-name@yandex.ru'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = 'some-pass'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'site_app',
    'personnel',
    'items',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# GETTING-STARTED: change 'site_app' to your project name:
ROOT_URLCONF = 'site_app.urls'

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
            ],
        },
    },
]

AUTH_USER_MODEL = 'personnel.Contact'
WSGI_APPLICATION = 'site_app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

if ON_PRODUCTION:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',  
            'NAME':     os.environ['OPENSHIFT_APP_NAME'],
            'USER':     os.environ['OPENSHIFT_POSTGRESQL_DB_USERNAME'],
            'PASSWORD': os.environ['OPENSHIFT_POSTGRESQL_DB_PASSWORD'],
            'HOST':     os.environ['OPENSHIFT_POSTGRESQL_DB_HOST'],
            'PORT':     os.environ['OPENSHIFT_POSTGRESQL_DB_PORT'],
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',  
            'NAME':     'django_1',
            'USER':     'django_1',
            'PASSWORD': '123',
            'HOST':     'localhost',
            'PORT':     '5432',
        }
    }



# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         # GETTING-STARTED: change 'db.sqlite3' to your sqlite3 database:
#         'NAME': os.path.join(DATA_DIR, 'db.sqlite3'),
#     }
# }

# Caching
# http://djbook.ru/rel1.9/topics/cache.html#local-memory-caching

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'm-site',
        'TIMEOUT': 60,
        'OPTIONS': {
            'MAX_ENTRIES': 1000
        }
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGES = (
    ('en', _('English')),
    ('ru', _('Russian')),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, '.i18n'),
)

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)


STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(REPO_DIR, '.static')

# STATICFILES_DIRS = [STATIC_ROOT]
# STATIC_ROOT = ''

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(REPO_DIR, '.media')


try:
    from site_app.local_settings import *
except ImportError as e:
    print('No local settings found')

if DEBUG:
    print('Project paths:')
    print('DJ_PROJECT_DIR: ', DJ_PROJECT_DIR)
    print('BASE_DIR: ', BASE_DIR)
    print('WSGI_DIR: ', WSGI_DIR)
    print('REPO_DIR: ', REPO_DIR)
    print('DATA_DIR: ', DATA_DIR)
    print('STATIC_ROOT: ', STATIC_ROOT)
    print('MEDIA_ROOT: ', MEDIA_ROOT)