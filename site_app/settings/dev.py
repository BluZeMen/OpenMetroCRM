from .common import *

ALLOWED_HOSTS = [
                    '109.234.37.121',
                    '127.0.0.1',
                    'localhost',
                ] + SECRETS.get('allowed_hosts', [])

DEBUG = True
ON_PRODUCTION = 'IS_PRODUCTION' in os.environ

if not ON_PRODUCTION and DEBUG:
    print("*** Warning - Debug mode is on ***")

THUMBNAIL_DEBUG = DEBUG

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'trololololol',
    },
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

MEDIA_ROOT = str(DATA_DIR.joinpath('static_content', 'media_root'))

SESSION_COOKIE_SECURE = False

STATIC_ROOT = str(DATA_DIR.joinpath('static_content', 'static_root'))

# django-push settings

PUSH_SSL_CALLBACK = False

# Enable optional components

if DEBUG:
    try:
        import debug_toolbar  # NOQA
    except ImportError:
        pass
    else:
        INSTALLED_APPS.append('debug_toolbar')
        INTERNAL_IPS = ['127.0.0.1']
        MIDDLEWARE.insert(
            MIDDLEWARE.index('django.middleware.common.CommonMiddleware') + 1,
            'debug_toolbar.middleware.DebugToolbarMiddleware'
        )
