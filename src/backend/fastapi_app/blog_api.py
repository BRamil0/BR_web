import datetime
import typing

from fastapi import APIRouter, Depends
from starlette.responses import RedirectResponse

from src.backend.fastapi_app import auth_utils
from src.backend.fastapi_app import models
from src.backend.database.database import DataBase, SearchTypeForPost
from src.backend.database.models import PostModel

router = APIRouter(
    prefix="/api/blog",
    tags=["blog_api"],
)

async def get_database() -> typing.AsyncGenerator[DataBase, None]:
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

@router.get("/get_post/{post_url}")
async def get_post(post_url: str, db: DataBase = Depends(get_database)):
    post = await db.get_post(SearchTypeForPost.url, post_url)
    if not post: post = await db.get_post(SearchTypeForPost.id, post_url)
    return {"post": post}

@router.post("/create_post")
async def create_post(post: models.CreatePostModel, db: DataBase = Depends(get_database), token_data: dict = Depends(auth_utils.token_verification)):
    new_post = PostModel(
        **post.model_dump(exclude_unset=True),
        user_id=token_data["id"],
        created_at=datetime.datetime.now(datetime.timezone.utc),
        updated_at=datetime.datetime.now(datetime.timezone.utc),
    )
    is_created = await db.create_post(new_post)

    return {"ok": is_created}