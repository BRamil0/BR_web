import slowapi
from fastapi.templating import Jinja2Templates
from slowapi.util import get_remote_address

from src.config.config import settings

templates = Jinja2Templates(directory="src/frontend/templates")
templates.env.globals["DEBUG_MODE"] = settings.DEBUG
templates.env.globals["experimental_functions"] = settings.experimental_functions
templates.env.globals["server_version"] = settings.server_version
templates.env.globals["api_version"] = settings.api_version

limiter = slowapi.Limiter(key_func=get_remote_address)
