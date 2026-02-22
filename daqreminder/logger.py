from logging import config, getLogger

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
    "loggers": {
        "root": {
            "level": "DEBUG",
            "handlers": ["rich"],
        },
    },
}

logger = getLogger("daqreminder")


def setup_logging():
    config.dictConfig(LOGGING_CONFIG)
