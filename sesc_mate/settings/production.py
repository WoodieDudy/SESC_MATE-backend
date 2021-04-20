import os

from logdna import LogDNAHandler

from .base import *

DEBUG = True

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    'sc-pri1b.michiru.sh',
    'sc-alt0a.michiru.sh'
]

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
}

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': 'localhost:6379',
        'OPTIONS': {
            'PARSER_CLASS': 'redis.connection.HiredisParser',
            'SERIALIZER_CLASS': 'redis_cache.serializers.JSONSerializer',
            'DB': 8,
        }
    },
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'sesc',
        'USER': 'sescuser',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '',
    }
}

VK_BOT_TOKEN = 'token'
VK_GROUP_ID = 186607004
BOT_USERNAME = '[club186607004|@sescmate]'

CELERY_DEBUG_MODE = 'sesc_mate.settings.production'
CELERY_TIMER = '*/15'

TELEGRAM_TOKEN = 'token'
LOGGING_TELEGRAM_CHAT_ID = -1001161129048

LOGDNA_KEYS = os.environ.get('INGESTION_KEYS').split(',') if 'INGESTION_KEYS' in os.environ else []
LOGDNA_HANDLERS = {f'logdna_{index}': {
    'level': 'DEBUG',
    'class': 'logging.handlers.LogDNAHandler',
    'key': key,
    'options': {
        'app': 'SESC MATE',
        'index_meta': True,
    },
} for key, index in zip(LOGDNA_KEYS, range(len(LOGDNA_KEYS)))}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'telegram': {
            '()': 'utils.html_formatter.FixedHtmlFormatter',
            'format': '<code>%(asctime)s</code> <b>%(levelname)s</b>\nFrom %(name)s:%(funcName)s\n%(message)s',
            # 'use_emoji': True
        }
    },
    'handlers': {
        **LOGDNA_HANDLERS,
        'console': {
            'class': 'logging.StreamHandler',
        },
        'telegram': {
            'class': 'telegram_handler.TelegramHandler',
            'token': TELEGRAM_TOKEN,
            'chat_id': LOGGING_TELEGRAM_CHAT_ID,
            'level': 'ERROR',
            'formatter': 'telegram'
        }
    },
    'root': {
        'handlers': ['telegram'],
        'level': 'DEBUG',
    },
    'loggers': {
        'logdna': {
            'handlers': LOGDNA_HANDLERS.keys(),
            'level': 'DEBUG'
        },
    },
}
