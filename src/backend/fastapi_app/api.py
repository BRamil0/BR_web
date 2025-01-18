import random

from fastapi import APIRouter, Request

from src.backend.fastapi_app import models
from src.config.config import settings
from src.backend.core.router_config import limiter

router = APIRouter(
    prefix="/api",
    tags=["api"],
)

not_use: list[int] = [2, 10, 12, 15]


@router.get("/background")
@limiter.limit("5/1c")
async def background(request: Request):
    while True:
        ran: int = random.randint(1, 20)
        if int(ran) not in not_use:
            break

    return {"image4k": f"/static/image/background/jpg/{ran}.jpg",
            "image2k": f"/static/image/background/2k/{ran}.webp",
            "image1k": f"/static/image/background/1k/{ran}.webp",}

@router.get("/background/{background_id}")
@limiter.limit("5/1c")
async def background(request: Request, background_id: int):
    return {"image4k": f"/static/image/background/jpg/{background_id}.jpg",
            "image2k": f"/static/image/background/2k/{background_id}.webp",
            "image1k": f"/static/image/background/1k/{background_id}.webp",}

@router.get("/theme_list", response_model=models.ThemeDefaultListModel)
@limiter.limit("5/1c")
async def theme_list(request: Request):
    return {"theme_list": settings.default_theme_list}

@router.get("/language_list", response_model=models.LanguageDefaultListModel)
@limiter.limit("5/1c")
async def language_list(request: Request):
    return {"language_list": settings.default_list_of_languages}

@router.get("/default_theme", response_model=models.ThemeDefaultModel)
@limiter.limit("5/1c")
async def default_theme(request: Request):
    return {"theme_default": settings.default_theme}

@router.get("/default_language", response_model=models.LanguageDefaultModel)
@limiter.limit("5/1c")
async def default_language(request: Request):
    return {"language_default": settings.default_language}

@router.get("/info", response_model=models.InfoAPIModel)
@limiter.limit("5/1c")
async def info(request: Request):
    return {"debug_mode": settings.DEBUG,
            "experimental_functions": settings.experimental_functions,
            "server_version": settings.server_version,
            "api_version": settings.api_version}

@router.get("/info/debug_mode")
@limiter.limit("5/1c")
async def debug_mode(request: Request):
    return {"debug_mode": settings.DEBUG}

@router.get("/info/experimental_functions")
@limiter.limit("5/1c")
async def experimental_functions(request: Request):
    return {"experimental_functions": settings.experimental_functions}

@router.get("/info/server_version")
@limiter.limit("5/1c")
async def server_version(request: Request):
    return {"server_version": settings.server_version}

@router.get("/info/api_version")
@limiter.limit("5/1c")
async def api_version(request: Request):
    return {"api_version": settings.api_version}