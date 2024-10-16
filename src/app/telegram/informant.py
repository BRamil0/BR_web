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
        print("ok")
        ip_main = IP(request)
        ip = await ip_main.get_client_ip()

        chat_id = settings.TELEGRAM_CHAT_ID
        params = {
            "chat_id": chat_id,
            "text": f"{form.message}\n`{await ip_main.summarize_location()}`"
        }
        async with self.session.post(self.url, json=params) as response:
            print("ok 2")
            return await response.json()
