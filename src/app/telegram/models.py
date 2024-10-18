from pydantic import BaseModel

class TelegramMessage(BaseModel):
    message: str

class TelegramInformant(BaseModel):
    innerWidth: str
    innerHeight: str
    screen_width: str
    screen_height: str
    userAgent: str
    platform: str
    language: str
    location_href: str
    connection_downlink: str
    connection_effective_type: str
    online: str
    performance_timing: str
    max_touch_points: str
    hardware_concurrency: str
    device_memory: str
    color_depth: str
    pixel_depth: str
    timezone: str
    cookies_enabled: str
    referrer: str
    visibility_state: str
    document_title: str
    page_load_time: str