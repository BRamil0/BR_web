from fastapi import APIRouter, status
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.telegram.models import TelegramInformant, TelegramMessage
from src.telegram import informant
import message

router = APIRouter(
    prefix="/api/telegram",
    tags=["telegram_api"],
)

@router.post("/info")
async def info(request: Request, tt: TelegramInformant):
    ts = informant.TelegramSender()
    shipment_status = await ts.send(request, tt)

    if shipment_status["ok"]:
        return JSONResponse({"ok": True}, status_code=status.HTTP_200_OK)
    return JSONResponse({"ok": False}, status_code=status.HTTP_400_BAD_REQUEST)


@router.post("/message")
async def send_message(request: Request, tms: TelegramMessage):
    ts = message.TelegramSender()
    shipment_status = await ts.send(request, tms)

    if shipment_status["ok"]:
        return JSONResponse({"ok": True}, status_code=status.HTTP_200_OK)
    return JSONResponse({"ok": False}, status_code=status.HTTP_400_BAD_REQUEST)