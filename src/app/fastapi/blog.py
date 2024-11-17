import datetime
from typing import AsyncGenerator

from fastapi import APIRouter, Depends
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.requests import Request

from src.app.database.database import DataBase
from src.app.fastapi.templates import templates

router = APIRouter(
    prefix="/blog",
    tags=["blog"],
)

async def get_database() -> AsyncGenerator[DataBase, None]:
    db = DataBase("blogs")
    try:
        yield db
    finally:
        await db.close_connection()


def format_date(value: datetime.datetime) -> str:
    return value.strftime("%Y-%m-%d")
templates.env.filters["format_date"] = format_date


@router.get("/post_list", response_class=HTMLResponse)
async def post_list(request: Request, db: DataBase = Depends(get_database)):
    posts = await db.get_all_posts()
    return templates.TemplateResponse("post_list.html", {"request": request, "posts": posts, "title": "Список постів"})


@router.get("/post")
async def post_redirect():
    return RedirectResponse(url="/post_list")


@router.get("/post/{post_id}", response_class=HTMLResponse)
async def get_post(request: Request, post_id: int, db: DataBase = Depends(get_database)):
    post = await db.get_post_id(post_id)
    return templates.TemplateResponse("post.html", {"request": request, "post": post[0]})