import sys

from .base import *

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache_table',
        'OPTIONS': {
            'SERIALIZER_CLASS': 'redis_cache.serializers.JSONSerializer',
        }
    }
}

ALLOWED_HOSTS = [
    '2d875d358bff.ngrok.io',
    'localhost'
]

VK_BOT_TOKEN = 'token'
VK_GROUP_ID = 190429649
BOT_USERNAME = '[club190429649|@woodiedudytestbot]'

CELERY_DEBUG_MODE = 'sesc_mate.settings.debug'
CELERY_TIMER = '*/1'

""" Debug console logging """

LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout
        },
    },
    'loggers': {
        'logdna': {
            'handlers': ['console'],
            'level': 'DEBUG'
        },
    },
}
