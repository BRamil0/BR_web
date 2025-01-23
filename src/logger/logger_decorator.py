import functools

from src.logger.logger import database_log_func
from src.config.config import settings

def async_decorator_info_for_database_log_func(func):
    @functools.wraps(func)
    async def wrapper(self, *args, **kwargs):
        result = await func(self, *args, **kwargs)

        if settings.DEBUG_DATABASE:
            log_message = f"Modified count: {result}, args: {args, kwargs}"
        else:
            log_message = f"Modified count: DEBUG_DATABASE is False"

        await database_log_func(func.__name__, log_message, "INFO")
        return result
    return wrapper