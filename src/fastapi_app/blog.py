import datetime
import typing

from fastapi import APIRouter, Depends, Request
from starlette.responses import HTMLResponse, RedirectResponse

from src.fastapi_app import auth_utils
from src.database.database import DataBase, SearchTypeForPost
from src.backend.templates import templates

router = APIRouter(
    prefix="/blog",
    tags=["blog"],
)

async def get_database() -> typing.AsyncGenerator[DataBase, None]:
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


@router.get("/post/{post_url}", response_class=HTMLResponse)
async def get_post(request: Request, post_url: str, db: DataBase = Depends(get_database)):
    post = await db.get_post(SearchTypeForPost.url, post_url)
    if not post: post = await db.get_post(SearchTypeForPost.id, post_url)
    return templates.TemplateResponse("post.html", {"request": request, "post": post[0]})

@router.get("/create_post", response_class=HTMLResponse)
async def post_create(request: Request, token_data: dict = Depends(auth_utils.token_verification_no_exceptions)):
    if not token_data: return RedirectResponse("/account/login", status_code=302)
    return templates.TemplateResponse("post_create.html", {"request": request})