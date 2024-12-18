import datetime
import typing
import bleach

import jwt
import argon2
import bson
from fastapi import HTTPException, Depends, Response, Request
import fastapi.security

from src.config.config import settings
from src.database.database import DataBase, SearchTypeForUser
from src.database import models
from src.logger.logger import logger

oauth2_scheme = fastapi.security.OAuth2PasswordBearer(tokenUrl="/api/auth/login", scheme_name="Bearer")
ph = argon2.PasswordHasher()

async def get_database() -> typing.AsyncGenerator[DataBase, None]:
    db = DataBase("account_info")
    try:
        yield db
    finally:
        await db.close_connection()

async def data_verification(data: dict[str, dict]) -> bool:
    for key, value in data.items():
        validator = value.get("validator")
        if not validator(value["value"]) and bleach.clean(value["value"]) != value["value"]:
            raise HTTPException(status_code=400, detail=f"{key} contains invalid characters or incorrect length")
    return True

async def sanitize_user_data(user: models.UserModel) -> dict:
    user_data = user.model_dump(exclude={"password", "oauth_links"})
    temp_id = 0

    for session in user_data.get("login_sessions", []):
        session["token"] = "REDACTED"
        session["login_time"] = str(session["login_time"].isoformat())
        session["temp_id"] = temp_id
        temp_id += 1

    for role in user_data.get("roles", []):
        role["id"] = str(role["id"])
        if role["at_added"] is not None: role["at_added"] = str(role["at_added"].isoformat())
        if role["at_works_until"] is not None: role["at_works_until"] = str(role["at_works_until"].isoformat())

    user_data["id"] = str(user_data["id"])
    user_data["created_at"] = str(user_data["created_at"].isoformat())
    user_data["updated_at"] = str(user_data["updated_at"].isoformat())

    return user_data


async def authenticate_user(db: DataBase, email: str, password: str):
    user = await db.get_user(SearchTypeForUser.email, email)
    try:
        if user and ph.verify(user.password, password):
            return user
    except argon2.exceptions.VerifyMismatchError:
        return False
    return False

async def token_verification(request: Request, db: DataBase = Depends(get_database)) -> dict:
    token = request.headers.get("Authorization")
    if token:
        scheme, token = token.split(" ", 1)
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid authentication scheme")
    else:
        token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=401, detail="Token not provided")
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
            options={"verify_exp": False}
        )
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    if payload.get("exp") < datetime.datetime.now().timestamp():
        await db.remove_login_session(payload.get("id"), token)
        raise HTTPException(status_code=401, detail="Token has expired")
    try:
        tokens_db = await db.get_login_sessions(payload.get("id"))
    except:
        raise HTTPException(status_code=403, detail="token not found")
    for token_db in tokens_db:
        if token_db["token"] == token:
            if token_db["is_active"]:
                payload["token"] = token
                return payload
            break

    raise HTTPException(status_code=401, detail="The token is not active")


async def token_verification_no_exceptions(request: Request, db: DataBase = Depends(get_database)) -> dict | None:
    try:
        return await token_verification(request, db)
    except HTTPException:
        return None

async def checking_tokens_relevance(user_id: str, db: DataBase = Depends(get_database)) -> bool:
    tokens = await db.get_login_sessions(user_id)
    if not tokens:
        return False
    for token in tokens:
        jwt_token = token["token"]
        try:
            payload = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        except jwt.ExpiredSignatureError:
            await db.remove_login_session(user_id, token)
            continue
        if payload.get("exp") < datetime.datetime.now().timestamp():
            await db.remove_login_session(user_id, token)
    return True

async def create_access_token(data: dict, expires_delta: datetime.timedelta = datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    expire = datetime.datetime.now(datetime.timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

async def add_new_login(user_id: bson.ObjectId, access_token: str, request:Request, device_name: str, db: DataBase = Depends(get_database)):
    ip_address = request.headers.get("X-Real-IP") or request.headers.get("X-Forwarded-For") or request.client.host
    user_agent = request.headers.get("User-Agent")
    if not isinstance(ip_address, str):
        ip_address = "unknown"
    if not isinstance(user_agent, str):
        user_agent = "unknown"

    if not ip_address or not user_agent:
        logger.opt(colors=True).warning(f"<blue>Auth</blue> | <c>Missing IP or User-Agent for user <b>{user_id}</b></c>")

    session_data = {
        "token": access_token,
        "device_name": device_name,
        "user_agent": user_agent,
        "is_active": True,
        "login_time": datetime.datetime.now(),
        "ip_address": ip_address
    }
    await db.add_login_session(user_id, session_data)

async def set_cookie(response: Response, access_token: str) -> None:
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=180 * 24 * 60 * 60,  # 180 днів у секундах
        secure=settings.SECURE_COOKIES,
        samesite="Lax"
    )