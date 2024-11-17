import sys

from loguru import logger
from fastapi import Request
from functools import wraps

from src.config.config import settings

logger.remove()

logger.add(sys.stdout, colorize=True, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | {message}")
logger.add("logs/app.log", rotation="10 MB", enqueue=True, backtrace=True, diagnose=True)
logger.add("logs/errors.log", level="ERROR", rotation="10 MB", enqueue=True, backtrace=True, diagnose=True)

def async_decorator_info_for_database_log_func(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        result = await func(self, *args, **kwargs)

        if settings.DEBUG_DATABASE:
            log_message = f"Modified count: {result}, args: {args, kwargs}"
        else:
            log_message = f"Modified count: DEBUG_DATABASE is False"

        await database_log_func(func.__name__, log_message, "INFO")
        return result
    return wrapper

async def log_requests(request: Request, call_next):
    response = await call_next(request)
    logger.opt(colors=True).info(f"<blue>FastAPI</blue> | <c>Status code: </c><b><m>{response.status_code}</m></b> | <c>Client IP:</c> <b><m>{request.client[0]}</m></b> | <c>Client port:</c> <b><m>{request.client[1]}</m></b> | <c>Request: <b><m>{request.method}</m> {request.url}</b></c>")
    return response

async def database_log_func(function_name: str, message: str = "", level: str = "INFO"):
    log_message = f"<blue>DataBase</blue> | <c>Function:</c> <b><m>{function_name}</m></b> | <c>Message</c> <b><m>{message}</m></b>"
    logger.opt(colors=True).log(level, log_message)
