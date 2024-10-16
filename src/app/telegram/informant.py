"""Partially by the author: Weever, modified by BRamil. Github: https://github.com/Weever1337"""

import aiohttp
from fastapi import Request
from typing import Dict, Any
from .models import TelegramMessage
from .ip_handler import IPAddressHandler as IP
from src.config.config import settings


class TelegramSender:
    def __init__(self) -> None:
        self.url = f"https://api.telegram.org/bot{settings.BOT_TOKEN}/sendMessage?parse_mode=markdown"
        self.session = aiohttp.ClientSession()

    async def send(self, request: Request, form: TelegramMessage) -> Dict[str, Any]:
        print(form, " ", request)
        ip = IP(request)
        chat_id = settings.TELEGRAM_CHAT_ID
        params = {
            "chat_id": chat_id,
            "text": f"{form.message}\n`{await ip.summarize_location()}\n`"
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(self.url, json=params) as response:
                print(await response.json())
                return await response.json()
