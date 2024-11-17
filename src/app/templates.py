from fastapi.templating import Jinja2Templates
from src.config.config import settings

templates = Jinja2Templates(directory="src/templates")
templates.env.globals["DEBUG_MODE"] = settings.DEBUG