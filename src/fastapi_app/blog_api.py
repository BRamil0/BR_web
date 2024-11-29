import datetime
import typing

from fastapi import APIRouter, Depends
from starlette.responses import RedirectResponse

from src.fastapi_app import auth_utils
from src.fastapi_app import models
from src.database.database import DataBase
from src.database.models import PostModel

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

@router.get("/get_post/{post_id}")
async def get_post(post_id: int, db: DataBase = Depends(get_database)):
    return await db.get_post_id(post_id)

@router.post("/create_post")
async def create_post(post: models.CreatePostModel, db: DataBase = Depends(get_database), token_data: dict = Depends(auth_utils.token_verification)):
    content = {
        "title": post.title,
        "content": post.content,
        "author": post.author,
        "language": post.language,
        "description": post.description,
        "image": post.image
    }

    new_post = PostModel(contents=content,
                         user_id=token_data["id"],
                         URL=post.URL,
                         created_at=datetime.datetime.now(datetime.timezone.utc),
                         updated_at=datetime.datetime.now(datetime.timezone.utc),
                         default_image=post.default_image)
    is_created = await db.create_post(new_post)

    return {"ok": is_created}