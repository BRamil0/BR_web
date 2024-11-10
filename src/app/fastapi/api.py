import random

from fastapi import APIRouter
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from src.app.database import models
from src.app.database.database import DataBase

router = APIRouter(
    prefix="/api",
)
templates = Jinja2Templates(directory="src/templates")
not_use: list[int] = [2, 10, 12, 15]

@router.get("/post_list/")
async def post_list():
    db = DataBase("blogs")
    return {"posts": await db.get_all_posts()}

@router.get("/get_post/")
async def get_post_list():
    return RedirectResponse(url="/post_list/")

@router.get("/get_post/{post_id}")
async def get_post(post_id: int):
    db = DataBase("blogs")
    return await db.get_post_id(post_id)

@router.post("/create_post")
async def create_post(post: models.CreatePostModel):
    db = DataBase("blogs")
    is_created = await db.create_post(post)
    return {"ok": is_created}

@router.get("/background")
async def background():
    while True:
        ran: int = random.randint(1, 20)
        if int(ran) not in not_use:
            break

    return {"image4k": f"/static/image/background/jpg/{ran}.jpg",
            "image2k": f"/static/image/background/2k/{ran}.webp",
            "image1k": f"/static/image/background/1k/{ran}.webp",}
