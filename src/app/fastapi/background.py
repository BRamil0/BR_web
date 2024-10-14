import random

from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from starlette.requests import Request


router = APIRouter()
templates = Jinja2Templates(directory="src/templates")


@router.get("/background")
async def background(request: Request):
    ran = random.randint(1, 10)
    return {"image4k": f"/static/image/background/4k/{ran}.webp",
            "image2k": f"/static/image/background/2k/{ran}.webp",
            "image1k": f"/static/image/background/1k/{ran}.webp",}