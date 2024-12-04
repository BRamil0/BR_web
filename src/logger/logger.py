import sys

from loguru import logger
from fastapi import Request

async def log_requests(request: Request, call_next):
    response = await call_next(request)
    logger.opt(colors=True).info(f"<le><b>FastAPI</b></le> | <lc>Status code: </lc><b><m>{response.status_code}</m></b> | <lc>Client IP:</lc> <b><m>{request.client[0]}</m></b> | <lc>Client port:</lc> <b><m>{request.client[1]}</m></b> | <lc>Request: <b><m>{request.method}</m> {request.url}</b></lc>")
    return response

async def database_log_func(function_name: str, message: str = "", level: str = "INFO"):
    log_message = f"<le><b>DataBase</b></le> | <le>Function: <b><lm>{function_name}</lm></b></le>  | <lc>Message</lc> <b><m>{message}</m></b>"
    logger.opt(colors=True).log(level, log_message)

logger.remove()
logger.add(sys.stdout, colorize=True, format="<y>IDP:{process}</y> <ly>SPT:{elapsed}</ly> | <g>{time:YYYY-MM-DD}</g> <lg>{time:HH:mm:ss}</lg> | <level>{level}</level> | <m>F:{file}</m> <lm>L:{line} FU:{function}</lm> | {message}")