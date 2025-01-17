import random

from fastapi import APIRouter

from src.backend.fastapi_app import models
from src.config.config import settings

router = APIRouter(
    prefix="/api",
    tags=["api"],
)

not_use: list[int] = [2, 10, 12, 15]



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

@router.get("/theme_list", response_model=models.ThemeDefaultListModel)
async def theme_list():
    return {"theme_list": settings.default_theme_list}

@router.get("/language_list", response_model=models.LanguageDefaultListModel)
async def language_list():
    return {"language_list": settings.default_list_of_languages}

@router.get("/default_theme", response_model=models.ThemeDefaultModel)
async def default_theme():
    return {"theme_default": settings.default_theme}

@router.get("/default_language", response_model=models.LanguageDefaultModel)
async def default_language():
    return {"language_default": settings.default_language}

@router.get("/info", response_model=models.InfoAPIModel)
async def info():
    return {"debug_mode": settings.DEBUG,
            "experimental_functions": settings.experimental_functions,
            "server_version": settings.server_version,
            "api_version": settings.api_version}

@router.get("/info/debug_mode")
async def debug_mode():
    return {"debug_mode": settings.DEBUG}

@router.get("/info/experimental_functions")
async def experimental_functions():
    return {"experimental_functions": settings.experimental_functions}

@router.get("/info/server_version")
async def server_version():
    return {"server_version": settings.server_version}

@router.get("/info/api_version")
async def api_version():
    return {"api_version": settings.api_version}