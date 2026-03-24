import logging
import os
import sys
from logging.config import dictConfig


# Define the log level mapping
LOG_LEVELS = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}

ENVIRONMENT = os.getenv("ENVIRONMENT", "development").lower()

# Set the log level based on the environment
if ENVIRONMENT == "development":
    DEFAULT_LOG_LEVEL = "DEBUG"
else:
    DEFAULT_LOG_LEVEL = "INFO"

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s %(asctime)s - %(message)s", 
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "use_colors": ENVIRONMENT == "development",
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "level": DEFAULT_LOG_LEVEL, 
        },
    },
    "loggers": {
        "my_fastapi_app": {
            "handlers": ["default"],
            "level": DEFAULT_LOG_LEVEL,
            "propagate": False,
        },
        "uvicorn": {
             "handlers": ["default"],
             "level": DEFAULT_LOG_LEVEL,
             "propagate": False,
        },
        "uvicorn.access": {
             "handlers": ["default"],
             "level": DEFAULT_LOG_LEVEL,
             "propagate": False, 
        },
    },
    "root": {
        "handlers": ["default"],
        "level": DEFAULT_LOG_LEVEL,
    },
}

# --- Initialization Function ---

def setup_logging():
    """Applies the dictionary configuration to the logging module."""
    dictConfig(LOGGING_CONFIG)

def get_app_logger(name: str):
    """
    Returns a logger instance for a specific module, using the main
    'my_fastapi_app' logger as a root for application logs.
    """
    return logging.getLogger(f"my_fastapi_app.{name}")

# Apply the configuration on import
setup_logging()