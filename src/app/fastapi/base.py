from fastapi import APIRouter, Response, Cookie
from starlette.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
router = APIRouter()
templates = Jinja2Templates(directory="src/templates")

@router.get("/", response_class=HTMLResponse)
async def index(request: Request, response: Response):
    response.set_cookie(key="language_code", value="ukr", httponly=True, samesite="None", secure=True)
    return templates.TemplateResponse("index.html", {"request": request, "title": "Головна"})


@router.get("/index", response_class=HTMLResponse)
async def index(request: Request, response: Response):
    response.set_cookie(key="language_code", value="ukr", httponly=True, samesite="None", secure=True)
    return templates.TemplateResponse("index.html", {"request": request, "title": "Головна"})
