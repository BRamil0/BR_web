import datetime

from fastapi import APIRouter
from starlette.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from src.app.database import models
from src.app.database.database import DataBase

router = APIRouter(
    prefix="/blog",
)
templates = Jinja2Templates(directory="src/templates")


def format_date(value: datetime.datetime) -> str:
    return value.strftime("%Y-%m-%d")
templates.env.filters["format_date"] = format_date


@router.get("/post_list", response_class=HTMLResponse)
async def post_list(request: Request):
    db = DataBase("blogs")
    posts = await db.get_all_posts()
    return templates.TemplateResponse("post_list.html", {"request": request, "posts": posts})


@router.get("/post")
async def post():
    return RedirectResponse(url="/post_list")


@router.get("/post/{post_id}", response_class=HTMLResponse)
async def get_post(request: Request, post_id: int):
    db = DataBase("blogs")
    post = await db.get_post_id(post_id)
    return templates.TemplateResponse("post.html", {"request": request, "post": post[0]})