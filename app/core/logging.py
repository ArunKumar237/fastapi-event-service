import logging
import sys
from typing import Dict
from pathlib import Path

_SERVICE_NAME = "event-service"

# Ensure logs directory exists
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

_LOGGERS: Dict[str, logging.Logger] = {}

_FORMATTER = logging.Formatter(
    fmt=(
        "ts=%(asctime)s "
        "level=%(levelname)s "
        "service=%(service)s "
        "module=%(name)s "
        "msg=\"%(message)s\""
    ),
    datefmt="%Y-%m-%dT%H:%M:%S",
)


class ContextFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.service = _SERVICE_NAME
        return True


# Console handler (stdout)
_CONSOLE_HANDLER = logging.StreamHandler(sys.stdout)
_CONSOLE_HANDLER.setFormatter(_FORMATTER)
_CONSOLE_HANDLER.addFilter(ContextFilter())

# File handler (persistent logs)
_FILE_HANDLER = logging.FileHandler(LOG_DIR / "app.log")
_FILE_HANDLER.setFormatter(_FORMATTER)
_FILE_HANDLER.addFilter(ContextFilter())


def get_logger(name: str) -> logging.Logger:
    if name in _LOGGERS:
        return _LOGGERS[name]

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    logger.addHandler(_CONSOLE_HANDLER)
    logger.addHandler(_FILE_HANDLER)

    logger.propagate = False

    _LOGGERS[name] = logger
    return logger
