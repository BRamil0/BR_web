import random

from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from src.config.config import settings

router = APIRouter(
    prefix="/api",
    tags=["api"],
)
templates = Jinja2Templates(directory="src/templates")
not_use: list[int] = [2, 10, 12, 15]

class ThemeModel(BaseModel):
    theme_list: list[str]

class LanguageModel(BaseModel):
    language_list: list[str]

@router.get("/background")
async def background():
    while True:
        ran: int = random.randint(1, 20)
        if int(ran) not in not_use:
            break

    return {"image4k": f"/static/image/background/jpg/{ran}.jpg",
            "image2k": f"/static/image/background/2k/{ran}.webp",
            "image1k": f"/static/image/background/1k/{ran}.webp",}

@router.get("/background/{background_id}")
async def background(background_id: int):
    return {"image4k": f"/static/image/background/jpg/{background_id}.jpg",
            "image2k": f"/static/image/background/2k/{background_id}.webp",
            "image1k": f"/static/image/background/1k/{background_id}.webp",}

@router.get("/theme_list", response_model=ThemeModel)
async def theme_list():
    return {"theme_list": settings.default_theme_list}

@router.get("/language_list", response_model=LanguageModel)
async def language_list():
    return {"language_list": settings.default_list_of_languages}
