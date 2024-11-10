from fastapi import APIRouter
from starlette.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from src.app.database import models
from src.app.database.database import DataBase

router = APIRouter(
    prefix="/blog",
)
templates = Jinja2Templates(directory="src/templates")


@router.get("/post_list", response_class=HTMLResponse)
async def post_list(request: Request):
    db = DataBase("blogs")
    return templates.TemplateResponse("post_list.html", {"request": request, "posts": await db.get_all_posts()})


@router.get("/post/{post_id}", response_class=HTMLResponse)
async def get_post(request: Request, post_id: int):
    db = DataBase("blogs")
    post = await db.get_post_id(post_id)
    return templates.TemplateResponse("post.html", {"request": request, "post": post[0]})