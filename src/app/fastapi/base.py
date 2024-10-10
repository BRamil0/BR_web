from fastapi import APIRouter
from pydantic import BaseModel
from starlette.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

import src.language.language

class LanguageCode(BaseModel):
    language_code: str

router = APIRouter()
templates = Jinja2Templates(directory="src/templates")

@router.get("/", response_class=HTMLResponse)
async def index(request: Request, language_code: LanguageCode):
    try:
        language = src.language.language.open_language_file(str(language_code["language_code"]))
    except KeyError:
        language = src.language.language.open_language_file("ukr")
    return templates.TemplateResponse("index.html", {"request": request,
                                                     "title": "Головна",
                                                     "language": language})

@router.get("/index", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "Головна"})
