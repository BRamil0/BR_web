from fastapi.templating import Jinja2Templates
from src.config.config import settings

templates = Jinja2Templates(directory="src/frontend/templates")
templates.env.globals["DEBUG_MODE"] = settings.DEBUG
templates.env.globals["experimental_functions"] = settings.experimental_functions
templates.env.globals["server_version"] = settings.server_version