from fastapi import APIRouter
from starlette.requests import Request
from src.app.telegram.models import TelegramInformant, TelegramMessage
from src.app.telegram import informant
from src.app.telegram import message

router = APIRouter()

@router.post("/info", status_code=200)
async def info(request: Request, tt: TelegramInformant):
    ts = informant.TelegramSender()
    await ts.send(request, tt)
    return {"ok": True}


@router.post("/message", status_code=200)
async def info(request: Request, tms: TelegramMessage):
    ts = message.TelegramSender()
    await ts.send(request, tms)
    return {"ok": True}
