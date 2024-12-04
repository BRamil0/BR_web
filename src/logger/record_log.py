import os
import loguru

from src.config.config import settings

def record_log(logger: loguru.logger) ->bool:
    if settings.is_log_record:
        logger.add(os.path.join(settings.log_dir, "app.log"), rotation="10 MB", enqueue=True, backtrace=True, diagnose=True)
        logger.add(os.path.join(settings.log_dir, "error.log"), level="ERROR", rotation="10 MB", enqueue=True, backtrace=True, diagnose=True)
        return True
    return False