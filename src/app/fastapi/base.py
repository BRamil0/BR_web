from fastapi import APIRouter
from starlette.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
router = APIRouter()
templates = Jinja2Templates(directory="src/templates")

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "Головна"})


@router.get("/index", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "Головна"})

@router.get("/terms_of_use", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("terms_of_use.html", {"request": request, "title": "Головна"})

@router.get("/privacy_policy", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("privacy_policy.html", {"request": request, "title": "Головна"})

@router.get("/cookie_policy", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("cookie_policy.html", {"request": request, "title": "Головна"})