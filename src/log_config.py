import logging
from enum import StrEnum

LOG_FORMAT_DEBUG = "%(levelname)s:%(message)s:%(pathname)s:%(funcName)s:%(lineno)d"

class LogLevels(StrEnum):
    debug = "DEBUG"
    info = "INFO"
    warning = "WARNING"
    error = "ERROR"
    critical = "CRITICAL"

def configure_logging(level: LogLevels.error):
    level = str(level).upper()
    levels = [level.value for level in LogLevels]

    if level not in levels:
        logging.basicConfig(level=logging.error)
        return

    if level == LogLevels.debug:
        logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT_DEBUG)

    logging.basicConfig(level=level)