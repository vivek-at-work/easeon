# -*- coding: utf-8 -*-
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
    "formatters": {
        "verbose": {"format": "[contactor] %(levelname)s %(asctime)s %(message)s"}
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "syslog": {
            "level": "DEBUG",
            "class": "logging.handlers.SysLogHandler",
            "facility": "local7",
            "address": "/dev/log",
            "formatter": "verbose",
        },
        "mail_admins": {
            "level": "WARNING",
            "class": "django.utils.log.AdminEmailHandler",
        },
    },
    "loggers": {
        "": {"handlers": ["syslog", "console"], "level": "INFO", "disabled": False},
        "easeon": {
            "handlers": ["syslog", "console"],
            "level": "ERROR",
            "disabled": False,
        },
    },
}
