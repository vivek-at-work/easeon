# -*- coding: utf-8 -*-
import environ

root = environ.Path(__file__) - 1  # three folder back (/a/b/c/ - 3 = /)
env = environ.Env(DEBUG=(bool, False))  # set default values and casting
environ.Env.read_env()  # reading .env file
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {'()': 'django.utils.log.RequireDebugFalse'}
    },
    'formatters': {
        'verbose': {
            'format': '[contactor] %(levelname)s %(asctime)s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'syslog': {
            'level': 'DEBUG',
            'class': 'logging.handlers.SysLogHandler',
            'facility': 'local7',
            'address': '/dev/log',
            'formatter': 'verbose',
        },
        # Warning messages are sent to admin emails
        'mail_admins': {
            'level': 'WARNING',
            'class': 'django.utils.log.AdminEmailHandler',
        },
    },
    'loggers': {
        # This is the "catch all" logger
        '': {
            'handlers': ['console', 'syslog'],
            'level': 'INFO',
            'disabled': False,
        },
        'thingsforwork': {
            'handlers': ['console', 'syslog'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
