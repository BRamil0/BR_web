from fastapi import APIRouter, Request
from starlette.responses import HTMLResponse

from src.app.templates import templates


router = APIRouter(
    prefix="/account",
    tags=["auth"],
)

@router.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request, "title": "Реєстрація"})


@router.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "title": "Вхід"})