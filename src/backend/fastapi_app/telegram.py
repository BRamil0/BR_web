import logging

from fastapi import APIRouter, status
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.backend.telegram.models import TelegramInformant, TelegramMessage
from src.backend.telegram import informant, message
from src.backend.core.router_config import limiter


router = APIRouter(
    prefix="/api/telegram",
    tags=["telegram_api"],
)

@router.post("/info")
@limiter.limit("10/10s")
async def info(request: Request, tt: TelegramInformant):
    try:
        ts = informant.TelegramSender()
        shipment_status = await ts.send(request, tt)

        if shipment_status["ok"]:
            return JSONResponse({"ok": True}, status_code=status.HTTP_200_OK)
    except BaseException as E:
        logging.error(f"{E}")
    return JSONResponse({"ok": False}, status_code=status.HTTP_400_BAD_REQUEST)


@router.post("/message")
@limiter.limit("4/10minutes")
async def send_message(request: Request, tms: TelegramMessage):
    try:
        ts = message.TelegramSender()
        shipment_status = await ts.send(request, tms)

        if shipment_status["ok"]:
            return JSONResponse({"ok": True}, status_code=status.HTTP_200_OK)
    except BaseException as E:
        logging.error(f"{E}")
    return JSONResponse({"ok": False}, status_code=status.HTTP_400_BAD_REQUEST)