import os

from src.logger.logger import logger

from src.config.config import settings
if settings.is_log_record or settings.DEBUG:
    logger.add(os.path.join(settings.log_dir, "app.log"), rotation="10 MB", enqueue=True, backtrace=True, diagnose=True)
    logger.add(os.path.join(settings.log_dir, "error.log"), level="ERROR", rotation="10 MB", enqueue=True, backtrace=True, diagnose=True)