from fastapi import APIRouter
from starlette.requests import Request
from src.app.telegram.models import TelegramMessage
from src.app.telegram.informant import TelegramSender

router = APIRouter()

@router.post("/info")
async def info(request: Request, tms: TelegramMessage):
    ts = TelegramSender()
    await ts.send(request, tms)
    return {"ok": True}