import os

if os.environ.get('MODE') == 'BAE':
    BASE_DIR = '/home/bae/log'
else:
    BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')

LOGGING = {
    'version': 1,
    'dusable_existing_loggers': True,
    'formatters': {
        'normal': {
            'format': '%(levelname)s %(asctime)s %(module)s %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(message)s'
            }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'django': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'D',
            'interval': 1,
            'backupCount': 5,
            'filename': os.path.join(BASE_DIR, 'django.log'),
            'formatter': 'normal'
        },
        'app': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'D',
            'interval': 1,
            'backupCount': 5,
            'filename': os.path.join(BASE_DIR, 'app.log'),
            'formatter': 'normal'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['django'],
            'propagate': False,
            'level': 'DEBUG'
        },
        '': {
            'handlers': ['app'],
            'level': 'DEBUG'
        }
    }
}
