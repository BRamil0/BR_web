from datetime import datetime, timedelta, timezone
from typing import AsyncGenerator

import jwt
from argon2 import PasswordHasher
from fastapi import APIRouter, HTTPException, Depends, Response, Request
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from src.config.config import settings
from src.app.database.database import DataBase
from src.app.database.models import UserModel

router = APIRouter(
    prefix="/api/auth",
    tags=["auth_api"],
)
ph = PasswordHasher()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

async def get_database() -> AsyncGenerator[DataBase, None]:
    db = DataBase("account_info")
    try:
        yield db
    finally:
        await db.close_connection()

async def authenticate_user(db: DataBase, email: str, password: str):
    user = await db.get_user_by_email(email)
    if user and ph.verify(user.password, password):
        return user
    return False

async def get_current_user(request: Request, db: DataBase = Depends(get_database)):
    token = request.cookies.get("access_token")
    if token is None:
        token = request.headers.get("Authorization")
        if token is None:
            raise HTTPException(status_code=401, detail="Token not provided")
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("exp") < datetime.now().timestamp():
            await db.remove_jwt_token(payload.get("sub"), token)
            raise HTTPException(status_code=401, detail="Token has expired")
        tokens_db = await db.get_jwt_tokens(payload.get("sub"))
        for token_db in tokens_db:
            if token_db["token"] == token:
                if token_db["is_active"]:
                    return payload
                else:
                    break
        raise HTTPException(status_code=401, detail="the token is not active")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

async def checking_tokens_relevance(user_id: str, db: DataBase = Depends(get_database)):
    tokens = await db.get_jwt_tokens(user_id)
    for token in tokens:
        jwt_token = token["jwt_token"]
        payload = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("exp") < datetime.now().timestamp():
            await db.remove_jwt_token(user_id, token)

async def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


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
async def register_user(user: UserCreate, response: Response, db: DataBase = Depends(get_database)):
    hashed_password = ph.hash(user.password)
    new_user = UserModel(
        username=user.username,
        email=[{"email": user.email, "is_verified": False}],
        password=hashed_password,
        is_active=True
    )
    user_created = await db.create_user(new_user)

    if not user_created:
        raise HTTPException(status_code=400, detail="User creation failed")

    user_db = await db.get_user_by_email(user.email)
    access_token = await create_access_token(data={"sub": user.email})
    await db.add_jwt_token(user_db.id, access_token, is_active=True)
    await set_cookie(response, access_token)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=Token)
async def login_user(email: str, password: str, response: Response, db: DataBase = Depends(get_database)):
    user = await authenticate_user(db, email, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = await create_access_token(data={"sub": email})
    await checking_tokens_relevance(user.id, db)
    await db.add_jwt_token(user.id, access_token, is_active=True)
    await set_cookie(response, access_token)
    return {"access_token": access_token, "token_type": "bearer"}