import random

from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from starlette.requests import Request


router = APIRouter()
templates = Jinja2Templates(directory="src/templates")


@router.get("/background")
async def background(request: Request):
    return {"image": f"/static/image/background/{random.randint(1, 10)}.jpg"}