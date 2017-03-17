from .common import *  # noqa

ALLOWED_HOSTS = [
                    '109.234.37.121',
                    '127.0.0.1',
                    'localhost',
                ] + SECRETS.get('allowed_hosts', [])

DEBUG = False
THUMBNAIL_DEBUG = DEBUG

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'django_site',
        'TIMEOUT': 60,
        'OPTIONS': {
            'MAX_ENTRIES': 1000
        }
    }

}

CSRF_COOKIE_SECURE = True

LOGGING["handlers"]["syslog"] = {
    "formatter": "full",
    "level": "DEBUG",
    "class": "logging.handlers.SysLogHandler",
    "address": "/dev/log",
    "facility": "local4",
}
LOGGING["loggers"]["django.request"]["handlers"].append("syslog")

MEDIA_ROOT = str(DATA_DIR.joinpath('media'))

# MIDDLEWARE = (
#     ['django.middleware.cache.UpdateCacheMiddleware'] +
#     MIDDLEWARE +
#     ['django.middleware.cache.FetchFromCacheMiddleware']
# )

SESSION_COOKIE_SECURE = True

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

STATIC_ROOT = str(DATA_DIR.joinpath('static'))

# # Log errors to Sentry instead of email, if available.
# if 'sentry_dsn' in SECRETS and not DEBUG:
#     INSTALLED_APPS.append('raven.contrib.django.raven_compat')
# RAVEN_CONFIG = {'dsn': SECRETS['sentry_dsn']}
