from fastapi import APIRouter
from starlette import status
from starlette.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

router = APIRouter()
templates = Jinja2Templates(directory="src/templates")

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "Головна"})

@router.get("/index")
async def not_found():
    return RedirectResponse(url="/")

@router.get("/terms_of_use", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("terms_of_use.html", {"request": request, "title": "Умови використання"})

@router.get("/privacy_policy", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("privacy_policy.html", {"request": request, "title": "Політика конфіденційності"})

@router.get("/cookie_policy", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("cookie_policy.html", {"request": request, "title": "Політика використання cookie"})

@router.get("/content_used", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("content_used.html", {"request": request, "title": "Використаний контент"})


@router.get("/contact", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request, "title": "Контакти"})


@router.get("/418", status_code=status.HTTP_418_IM_A_TEAPOT)
async def index(request: Request):
    return templates.TemplateResponse("code.html", {"request": request, "title": "code 418", "code": 418, "message": "I'm a teapot"})