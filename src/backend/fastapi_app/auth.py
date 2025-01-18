from fastapi import APIRouter, Request, Depends, HTTPException
from starlette.responses import HTMLResponse, RedirectResponse

from src.backend.database.database import DataBase, SearchTypeForUser
from src.backend.database import db_utils
from src.backend.core.router_config import templates
from src.backend.fastapi_app.auth_utils import token_verification_no_exceptions, get_database

router = APIRouter(
    prefix="/account",
    tags=["auth"],
)

@router.get("/register", response_class=HTMLResponse)
async def register(request: Request, token_data: dict = Depends(token_verification_no_exceptions)):
    if token_data:
        return RedirectResponse("/account/profile/my", status_code=302)
    return templates.TemplateResponse("register.html", {"request": request, "title": "Реєстрація"})


@router.get("/login", response_class=HTMLResponse)
async def login(request: Request, token_data: dict = Depends(token_verification_no_exceptions)):
    if token_data: return RedirectResponse("/account/profile/", status_code=302)
    return templates.TemplateResponse("login.html", {"request": request, "title": "Вхід"})

@router.get("/settings", response_class=HTMLResponse)
async def settings(request: Request, token_data: dict = Depends(token_verification_no_exceptions)):
    if not token_data: return RedirectResponse("/account/login", status_code=302)
    return templates.TemplateResponse("settings.html", {"request": request, "title": "Налаштування"})

@router.get("/control_panel", response_class=HTMLResponse)
async def control_panel(request: Request, db: DataBase = Depends(get_database), token_data: dict = Depends(token_verification_no_exceptions)):
    if not token_data: return RedirectResponse("/account/login", status_code=302)
    user = await db.get_user(SearchTypeForUser.id, token_data["id"])
    if await db_utils.is_permission_in_user(user.id, "root", db) or await db_utils.is_permission_in_user(user.id, "site_administration_panel", db):
        return templates.TemplateResponse("control_panel.html", {"request": request, "title": "Панель керування", "user": user})
    raise HTTPException(status_code=403, detail="User has no permission")

@router.get("/profile/", response_class=HTMLResponse)
async def profile():
    return RedirectResponse("/account/profile/my", status_code=302)

@router.get("/profile/my", response_class=HTMLResponse)
async def profile_my(request: Request, db: DataBase = Depends(get_database), token_data: dict = Depends(token_verification_no_exceptions)):
    if not token_data: return RedirectResponse("/account/login", status_code=302)
    user = await db.get_user(SearchTypeForUser.id, token_data["id"])
    return RedirectResponse(f"/account/profiles/{user.username}", status_code=302)

@router.get("/profiles/{username}", response_class=HTMLResponse)
async def profile(request: Request, username: str, db: DataBase = Depends(get_database)):
    user = await db.get_user(SearchTypeForUser.username, username)
    return templates.TemplateResponse("profile.html", {"request": request, "user": user, "title": f"Профіль {user.username}"})