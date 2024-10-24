"""Partially by the author: Weever, modified by BRamil. Github: https://github.com/Weever1337"""

import aiohttp
from fastapi import Request
from typing import Dict, Any
from .models import TelegramMessage
from .ip_handler import IPAddressHandler
from src.config.config import settings
from src.app.shielding import shielding_markdown_v2

class TelegramSender:
    def __init__(self) -> None:
        self.url = f"https://api.telegram.org/bot{settings.BOT_TOKEN}/sendMessage"

    async def send(self, request: Request, form: TelegramMessage) -> Dict[str, Any]:
        ip = IPAddressHandler(request)
        chat_id = settings.TELEGRAM_CHAT_ID

        comma = ","
        if form.author == "" and form.email == "":
            comma = ""

        params = {
            "chat_id": chat_id,
            "text": fr"""
Нове повідомлення:

*{await shielding_markdown_v2(form.name)}*

{await shielding_markdown_v2(form.message)}

{await shielding_markdown_v2(form.author)}{comma} {await shielding_markdown_v2(form.email)}
_Додаткова інформація:_
IP: `{ip.ip}`
Location: `{await ip.get_location()}`
User agent: `{request.headers.get("User-Agent")}` 
Language: `{request.headers.get("Accept-Language")}`

\#нове\_повідомлення
""",
            "parse_mode": "MarkdownV2",
        }
        print(params)
        async with aiohttp.ClientSession() as session:
            async with session.post(self.url, json=params) as response:
                print(await response.json())
                return await response.json()
