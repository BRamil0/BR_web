import datetime

import argon2
import bson
from fastapi import APIRouter, HTTPException, Depends, Response, Request
from starlette.responses import JSONResponse

from src.database.database import DataBase, SearchTypeForUser, SearchAttributeForUser
from src.database.models import UserModel
from src.backend import validators
from src.fastapi_app import auth_utils
from src.fastapi_app import models


router = APIRouter(
    prefix="/api/auth",
    tags=["auth_api"],
)
ph = argon2.PasswordHasher()

@router.post("/register", response_model=models.Token)
async def register_user(user: models.UserCreate, response: Response, request: Request, device_name: str | None = "unknown", db: DataBase = Depends(auth_utils.get_database)):
    for field, value in [("email", user.email), ("username", user.username)]:
        if await db.search_for_attribute_uniqueness(getattr(SearchAttributeForUser, field), {field: value}):
            raise HTTPException(status_code=400, detail=f"User with this {field} already exists")

    fields = {
        "username": {"value": user.username, "validator": validators.validate_username, },
        "email": {"value": user.email, "validator": validators.validate_email, },
        "password": {"value": user.password, "validator": validators.validate_password, },
        "device_name": {"value": device_name, "validator": lambda x: True, },
    }
    result = await auth_utils.data_verification(fields)
    if not result:
        raise HTTPException(status_code=400, detail="Invalid data")

    hashed_password = ph.hash(user.password)

    new_user = UserModel(
        username=user.username,
        email=[{"email": user.email, "is_verified": False}],
        password=hashed_password,
        is_active=True,
        roles=[],
        created_at=datetime.datetime.now(datetime.timezone.utc),
        updated_at=datetime.datetime.now(datetime.timezone.utc),
    )
    user_created = await db.create_user(new_user)

    if not user_created:
        raise HTTPException(status_code=400, detail="User creation failed")

    user_db = await db.get_user(SearchTypeForUser.email, user.email)
    access_token = await auth_utils.create_access_token(data={"id": str(user_db.id)})
    await auth_utils.add_new_login(user_db.id, access_token, request, device_name, db)
    await auth_utils.set_cookie(response, access_token)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=models.Token)
async def login_user(login_form: models.LoginForm, response: Response, request: Request, device_name: str | None = "unknown", db: DataBase = Depends(auth_utils.get_database)):
    fields = {
        "email": {"value": login_form.email, "validator": validators.validate_email, },
        "password": {"value": login_form.password, "validator": validators.validate_password, },
        "device_name": {"value": device_name, "validator": lambda x: True, },
    }
    result = await auth_utils.data_verification(fields)
    if not result:
        raise HTTPException(status_code=400, detail="Invalid data")

    user = await auth_utils.authenticate_user(db, login_form.email, login_form.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = await auth_utils.create_access_token(data={"id": str(user.id)})
    await auth_utils.checking_tokens_relevance(user.id, db)
    await auth_utils.add_new_login(user.id, access_token, request, device_name, db)
    await auth_utils.set_cookie(response, access_token)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/logout")
async def logout_user(response: Response, db: DataBase = Depends(auth_utils.get_database), token_date: dict[str, str] = Depends(
    auth_utils.token_verification)):
    await db.remove_login_session(bson.ObjectId(token_date["id"]), token_date["token"])
    response.delete_cookie(key="access_token")
    await auth_utils.checking_tokens_relevance(bson.ObjectId(token_date["id"]), db)
    return {"message": "Logged out successfully"}

@router.get("/current_user", response_model=models.ResponseModelForGetCurrentUser)
async def get_current_user(db: DataBase = Depends(auth_utils.get_database), token_date: dict[str, str] = Depends(auth_utils.token_verification_no_exceptions)):
    if not token_date:
        return JSONResponse(content={"message": "You are not logged in", "status": None})
    user = await db.get_user(SearchTypeForUser.id, token_date["id"])
    if user:
        date = {"message": "tokens and password were hidden for safety",
                "status": "ok",
                "user": await auth_utils.sanitize_user_data(user)}
        return JSONResponse(content=date)
    raise HTTPException(status_code=401, detail="User not found")

@router.post("/change_password")
async def change_password(password_change: models.PasswordChangeForm, db: DataBase = Depends(auth_utils.get_database), token_date: dict[str, str] = Depends(auth_utils.token_verification)):

    user = await db.get_user(SearchTypeForUser.id, token_date["id"])
    if not ph.verify(user.password, password_change.old_password):
        raise HTTPException(status_code=400, detail="Old password is incorrect")

    await auth_utils.data_verification({"password": {"value": password_change.new_password, "validator": validators.validate_password, }})

    new_hashed_password = ph.hash(password_change.new_password)
    await db.set_user_data(user.id, {"password": new_hashed_password})

    return {"message": "Password changed successfully"}

