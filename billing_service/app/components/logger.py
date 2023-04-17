from app.middlewares import x_request_id


def request_id_filter(record):
    record.request_id = x_request_id.get()
    return True


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
        "add_request_id": {
            "()": "django.utils.log.CallbackFilter",
            "callback": request_id_filter,
        },
    },
    "formatters": {
        "django.server": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[{server_time}] {message}",
            "style": "{",
        }
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
        },
        "django.server": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "django.server",
        },
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
        "logstash": {
            "level": "DEBUG",
            "class": "logstash.LogstashHandler",
            "host": "logstash",
            "port": 5044,
            "version": 1,
            "message_type": "logstash",
            "fqdn": False,
            "tags": ["admin-panel"],
            "filters": ["add_request_id"],
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "mail_admins", "logstash"],
            "level": "INFO",
        },
        "django.server": {
            "handlers": ["django.server"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
