import logging
import sys
from pythonjsonlogger import jsonlogger    # correct for version 4.x
from app.core.config import settings

def setup_logging():
    logger = logging.getLogger("mg_esign")
    logger.setLevel(settings.log_level)
    handler = logging.StreamHandler(sys.stdout)
    formatter = jsonlogger.JsonFormatter(
        "%(timestamp)s %(level)s %(name)s %(message)s"
    )
    handler.setFormatter(formatter)
    logger.handlers = [handler]
    return logger

logger = setup_logging()
