import os
from logging import config, getLogger

logger = getLogger("daqreminder")


def setup_logging():
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
    EXTRA_LOGGERS = os.getenv("EXTRA_LOGGERS", "")

    _extra_logger_names = [
        name.strip() for name in EXTRA_LOGGERS.split(",") if name.strip()
    ]

    _loggers_config = {
        "daqreminder": {
            "level": LOG_LEVEL,
            "handlers": ["rich"],
            "propagate": False,
        },
        "root": {
            "level": "WARNING",
            "handlers": ["rich"],
        },
    }

    for name in _extra_logger_names:
        _loggers_config[name] = {
            "level": LOG_LEVEL,
            "handlers": ["rich"],
            "propagate": False,
        }

    LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "rich": {
                "format": "%(message)s",
            },
        },
        "handlers": {
            "rich": {
                "class": "rich.logging.RichHandler",
                "level": "DEBUG",
                "formatter": "rich",
                "rich_tracebacks": True,
                "markup": True,
            },
        },
        "loggers": _loggers_config,
    }

    config.dictConfig(LOGGING_CONFIG)
