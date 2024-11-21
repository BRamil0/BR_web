import datetime
import typing

import bleach
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

async def get_database() -> typing.AsyncGenerator[DataBase, None]:
    db = DataBase("account_info")
    try:
        yield db
    finally:
        await db.close_connection()

@router.post("/register", response_model=models.Token)
async def register_user(user: models.UserCreate, response: Response, request: Request, device_name: str | None = "unknown", db: DataBase = Depends(get_database)):
    if await db.search_for_attribute_uniqueness(SearchAttributeForUser.email, {"email": user.email}):
       raise HTTPException(status_code=400, detail="User with this email already exists")
    if await db.search_for_attribute_uniqueness(SearchAttributeForUser.username, user.username):
       raise HTTPException(status_code=400, detail="User with this username already exists")

    if bleach.clean(user.username) != user.username or not await validators.validate_username(user.username):
        raise HTTPException(status_code=400, detail="Username contains invalid characters or incorrect length")

    if bleach.clean(user.email) != user.email or not await validators.validate_email(user.email):
        raise HTTPException(status_code=400, detail="Email contains invalid characters")

    if bleach.clean(user.password) != user.password or not await validators.validate_password(user.password):
        raise HTTPException(status_code=400, detail="Password contains invalid characters or incorrect length")

    if device_name != bleach.clean(device_name):
        raise HTTPException(status_code=400, detail="Device name contains invalid characters")

    hashed_password = ph.hash(user.password)

    new_user = UserModel(
        username=user.username,
        email=[{"email": user.email, "is_verified": False}],
        password=hashed_password,
        is_active=True,
        roles=["user"],
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
async def login_user(login_form: models.LoginForm, response: Response, request: Request, device_name: str | None = "unknown", db: DataBase = Depends(get_database)):
    if device_name != bleach.clean(device_name):
        raise HTTPException(status_code=400, detail="Device name contains invalid characters")

    user = await auth_utils.authenticate_user(db, login_form.email, login_form.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = await auth_utils.create_access_token(data={"id": str(user.id)})
    await auth_utils.checking_tokens_relevance(user.id, db)
    await auth_utils.add_new_login(user.id, access_token, request, device_name, db)
    await auth_utils.set_cookie(response, access_token)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/logout")
async def logout_user(response: Response, db: DataBase = Depends(get_database), token_date: dict[str, str] = Depends(
    auth_utils.token_verification)):
    await db.remove_login_session(bson.ObjectId(token_date["id"]), token_date["token"])
    response.delete_cookie(key="access_token")
    await auth_utils.checking_tokens_relevance(bson.ObjectId(token_date["id"]), db)
    return {"message": "Logged out successfully"}

@router.get("/current_user", response_model=models.ResponseModelForGetCurrentUser)
async def get_current_user(db: DataBase = Depends(get_database), token_date: dict[str, str] = Depends(
    auth_utils.token_verification)):
    user = await db.get_user(SearchTypeForUser.id, token_date["id"])
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    for i in range(len(user.login_sessions)):
        user.login_sessions[i]["token"] = None
        user.login_sessions[i]["temporary_ID"] = i
        user.login_sessions[i]["login_time"] = str(user.login_sessions[i]["login_time"].isoformat())

    user_data = user.model_dump(exclude={"password", "oauth_links"})
    user_data["id"] = str(user_data["id"])
    user_data["created_at"] = str(user_data["created_at"].isoformat())
    user_data["updated_at"] = str(user_data["updated_at"].isoformat())

    date = {"message": "tokens and password were hidden for safety",
            "status": "ok",
            "user": user_data}
    return JSONResponse(content=date)

@router.post("/change_password")
async def change_password(password_change: models.PasswordChangeForm, db: DataBase = Depends(get_database), token_date: dict[str, str] = Depends(
    auth_utils.token_verification)):
    user = await db.get_user(SearchTypeForUser.id, token_date["id"])
    if not ph.verify(user.password, password_change.old_password):
        raise HTTPException(status_code=400, detail="Old password is incorrect")
    if bleach.clean(password_change.new_password) != password_change.new_password or not await validators.validate_password(password_change.new_password):
        raise HTTPException(status_code=400, detail="Password contains invalid characters or incorrect length")
    new_hashed_password = ph.hash(password_change.new_password)
    await db.set_user_data(user.id, {"password": new_hashed_password})
    return {"message": "Password changed successfully"}