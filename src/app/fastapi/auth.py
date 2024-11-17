import re
from datetime import datetime, timedelta, timezone
from typing import AsyncGenerator, List, Dict, Union, Optional

import bleach
import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from bson import ObjectId
from fastapi import APIRouter, HTTPException, Depends, Response, Request
from fastapi.security import OAuth2PasswordBearer
from jwt import ExpiredSignatureError
from pydantic import BaseModel, EmailStr
from starlette.responses import JSONResponse

from src.config.config import settings
from src.app.database.database import DataBase, SearchTypeForUser, SearchAttributeForUser
from src.app.database.models import UserModel

router = APIRouter(
    prefix="/api/auth",
    tags=["auth_api"],
)
ph = PasswordHasher()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", scheme_name="Bearer")


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class LoginForm(BaseModel):
    email: str
    password: str

class PasswordChangeForm(BaseModel):
    old_password: str
    new_password: str

class ResponseModelForGetCurrentUser(BaseModel):
    class ModelUserForGetCurrentUser(BaseModel):
        id: str
        username: str
        email: List[Dict[str, Union[EmailStr, bool]]]
        phone_number: List[Dict[str, Union[str, bool]]]
        login_sessions: List[Dict[str, Union[str, bool]]]
        is_password_active: bool = True
        roles: List[Optional[str]]
        is_active: bool = False
        created_at: str
        updated_at: str
        about_me: str | None = None
        language: str | None = None
        theme: str | None = None
        avatar: str | None = None
        background_image: str | None = None

    user: list[ModelUserForGetCurrentUser]
    message: str
    status: str


async def get_database() -> AsyncGenerator[DataBase, None]:
    db = DataBase("account_info")
    try:
        yield db
    finally:
        await db.close_connection()

async def validate_username(username: str) -> bool:
    pattern = r'^[a-zA-Zа-яА-Я0-9_.\-+~?,:{}=&|`[\]]{2,128}$'
    return bool(re.match(pattern, username))

async def validate_email(email: str) -> bool:
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(email_pattern, email))

async def validate_password(password: str) -> bool:
    pattern = r'^(?=.*[a-zA-Zа-яА-Я])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>+=]).{6,128}$'
    return bool(re.match(pattern, password))

async def authenticate_user(db: DataBase, email: str, password: str):
    user = await db.get_user(SearchTypeForUser.email, email)
    try:
        if user and ph.verify(user.password, password):
            return user
    except VerifyMismatchError:
        return False
    return False

async def token_verification(request: Request, token: str = Depends(oauth2_scheme), db: DataBase = Depends(get_database)) -> dict:
    if token is None:
        token = request.cookies.get("access_token")
        if token is None:
            raise HTTPException(status_code=401, detail="Token not provided")
        token = token.replace("Bearer ", "")

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM], options={"verify_exp": False})
        if payload.get("exp") < datetime.now().timestamp():
            await db.remove_login_session(payload.get("id"), token)
            raise HTTPException(status_code=401, detail="Token has expired")

        tokens_db = await db.get_login_sessions(payload.get("id"))
        for token_db in tokens_db:
            if token_db["token"] == token:
                if token_db["is_active"]:
                    payload["token"] = token
                    return payload
                else:
                    break
        raise HTTPException(status_code=401, detail="The token is not active")

    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

async def checking_tokens_relevance(user_id: str, db: DataBase = Depends(get_database)) -> bool:
    tokens = await db.get_login_sessions(user_id)
    if not tokens:
        return False
    for token in tokens:
        jwt_token = token["token"]
        try:
            payload = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        except ExpiredSignatureError:
            await db.remove_login_session(user_id, token)
            continue
        if payload.get("exp") < datetime.now().timestamp():
            await db.remove_login_session(user_id, token)
    return True

async def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

async def add_new_login(user_id: ObjectId, access_token: str, request:Request, device_name: str, db: DataBase = Depends(get_database)):
    ip_address = request.headers.get("X-Real-IP") or request.headers.get("X-Forwarded-For") or request.client.host
    user_agent = request.headers.get("User-Agent")
    if not isinstance(ip_address, str):
        ip_address = "unknown"
    if not isinstance(user_agent, str):
        user_agent = "unknown"

    session_data = {
        "token": access_token,
        "device_name": device_name,
        "user_agent": user_agent,
        "is_active": True,
        "login_time": datetime.now(),
        "ip_address": ip_address
    }
    await db.add_login_session(user_id, session_data)

async def set_cookie(response: Response, access_token: str) -> None:
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=timedelta(days=180),
        expires=datetime.now(timezone.utc) + timedelta(days=180),
        secure=settings.SECURE_COOKIES,
        samesite="Strict"
    )

@router.post("/register", response_model=Token)
async def register_user(user: UserCreate, response: Response, request: Request, device_name: str | None = None, db: DataBase = Depends(get_database)):
    if await db.search_for_attribute_uniqueness(SearchAttributeForUser.email, {"email": user.email}):
       raise HTTPException(status_code=400, detail="User with this email already exists")
    if await db.search_for_attribute_uniqueness(SearchAttributeForUser.username, user.username):
       raise HTTPException(status_code=400, detail="User with this username already exists")

    if bleach.clean(user.username) != user.username or not await validate_username(user.username):
        raise HTTPException(status_code=400, detail="Username contains invalid characters or incorrect length")

    if bleach.clean(user.email) != user.email or not await validate_email(user.email):
        raise HTTPException(status_code=400, detail="Email contains invalid characters")

    if bleach.clean(user.password) != user.password or not await validate_password(user.password):
        raise HTTPException(status_code=400, detail="Password contains invalid characters or incorrect length")

    if device_name is None:
        device_name = "unknown"

    if device_name != bleach.clean(device_name):
        raise HTTPException(status_code=400, detail="Device name contains invalid characters")

    hashed_password = ph.hash(user.password)

    new_user = UserModel(
        username=user.username,
        email=[{"email": user.email, "is_verified": False}],
        password=hashed_password,
        is_active=True,
        roles=["user"],
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    user_created = await db.create_user(new_user)

    if not user_created:
        raise HTTPException(status_code=400, detail="User creation failed")

    user_db = await db.get_user(SearchTypeForUser.email, user.email)
    access_token = await create_access_token(data={"id": str(user_db.id)})
    await add_new_login(user_db.id, access_token, request, device_name, db)
    await set_cookie(response, access_token)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
async def login_user(login_form: LoginForm, response: Response, request: Request, device_name: str | None = None, db: DataBase = Depends(get_database)):
    if device_name is None:
        device_name = "unknown"
    if device_name != bleach.clean(device_name):
        raise HTTPException(status_code=400, detail="Device name contains invalid characters")

    user = await authenticate_user(db, login_form.email, login_form.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = await create_access_token(data={"id": str(user.id)})
    await checking_tokens_relevance(user.id, db)
    await add_new_login(user.id, access_token, request, device_name, db)
    await set_cookie(response, access_token)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/logout")
async def logout_user(response: Response, db: DataBase = Depends(get_database), token_date: dict[str, str] = Depends(token_verification)):
    await db.remove_login_session(ObjectId(token_date["id"]), token_date["token"])
    response.delete_cookie(key="access_token")
    await checking_tokens_relevance(ObjectId(token_date["id"]), db)
    return {"message": "Logged out successfully"}

@router.get("/current_user", response_model=ResponseModelForGetCurrentUser)
async def get_current_user(db: DataBase = Depends(get_database), token_date: dict[str, str] = Depends(token_verification)):
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
async def change_password(password_change: PasswordChangeForm, db: DataBase = Depends(get_database), token_date: dict[str, str] = Depends(token_verification)):
    user = await db.get_user(SearchTypeForUser.id, token_date["id"])
    if not ph.verify(user.password, password_change.old_password):
        raise HTTPException(status_code=400, detail="Old password is incorrect")
    if bleach.clean(password_change.new_password) != password_change.new_password or not await validate_password(password_change.new_password):
        raise HTTPException(status_code=400, detail="Password contains invalid characters or incorrect length")
    new_hashed_password = ph.hash(password_change.new_password)
    await db.set_user_data(user.id, {"password": new_hashed_password})
    return {"message": "Password changed successfully"}