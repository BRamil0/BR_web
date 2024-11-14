from typing import AsyncGenerator

from fastapi import APIRouter, Depends
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from src.app.database import models
from src.app.database.database import DataBase

router = APIRouter(
    prefix="/api/blog",
    tags=["blog_api"],
)
templates = Jinja2Templates(directory="src/templates")

async def get_database() -> AsyncGenerator[DataBase, None]:
    db = DataBase("blogs")
    try:
        yield db
    finally:
        await db.close_connection()

@router.get("/post_list/")
async def post_list(db: DataBase = Depends(get_database)):
    return {"posts": await db.get_all_posts()}

@router.get("/get_post/")
async def get_post_list():
    return RedirectResponse(url="/post_list/")

@router.get("/get_post/{post_id}")
async def get_post(post_id: int, db: DataBase = Depends(get_database)):
    return await db.get_post_id(post_id)

@router.post("/create_post")
async def create_post(post: models.CreatePostModel, db: DataBase = Depends(get_database)):
    is_created = await db.create_post(post)
    return {"ok": is_created}