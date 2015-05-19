from settings.common import *
import dj_database_url

# Parse database configuration from $DATABASE_URL
DATABASES['default'] = dj_database_url.config()

# mailgun
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.mailgun.org'
EMAIL_HOST_USER = os.environ.get('DJANGO_EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('DJANGO_EMAIL_HOST_PASSWORD', '')
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = 'noreply@pdcst.ninja'

# celery
BROKER_URL = os.environ.get('CLOUDAMQP_URL', '')

# logging
OPBEAT = {
    "ORGANIZATION_ID": os.environ.get('OPBEAT_ORGANIZATION_ID', ''),
    "APP_ID": os.environ.get('OPBEAT_APP_ID', ''),
    "SECRET_TOKEN": os.environ.get('OPBEAT_SECRET_TOKEN', '')
}
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'verbose_heroku': {
            'format': ('%(asctime)s [%(process)d] [%(levelname)s] ' +
                       'pathname=%(pathname)s lineno=%(lineno)s ' +
                       'funcname=%(funcName)s %(message)s'),
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        }
    },
    'handlers': {
        'opbeat': {
            'level': 'WARNING',
            'class': 'opbeat.contrib.django.handlers.OpbeatHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose_heroku'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'podcastninja': {
            'level': 'DEBUG',
            'handlers': ['opbeat', 'console'],
            'propagate': False,
        },
        # Log errors from the Opbeat module to the console (recommended)
        'opbeat.errors': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}
