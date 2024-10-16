"""the main application startup file"""

import asyncio

import uvicorn
import fastapi
from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from src.config.config import settings

from fastapi.templating import Jinja2Templates

from src.app.fastapi import base
from src.app.fastapi import background
from src.app.fastapi import telegram

def import_routers(app: fastapi.FastAPI) -> None:
    """
    import routers
    :param app: fastapi.FastAPI
    :return: None
    """
    app.include_router(base.router)
    app.include_router(background.router)
    app.include_router(telegram.router)


def init_codes(app: fastapi.FastAPI) -> None:
    """
    init codes
    :param app: fastapi.FastAPI
    :return: None
    """

    templates = Jinja2Templates(directory="src/templates")


    @app.exception_handler(400)
    async def custom_400_handler(request, __):
        return templates.TemplateResponse("code.html", {"request": request,
                                                        "title": "code 400",
                                                        "code": 400,
                                                        "message": "bad request"})

    @app.exception_handler(401)
    async def custom_401_handler(request, __):
        return templates.TemplateResponse("code.html", {"request": request,
                                                        "title": "code 401",
                                                        "code": 401,
                                                        "message": "unauthorized"})

    @app.exception_handler(403)
    async def custom_403_handler(request, __):
        return templates.TemplateResponse("code.html", {"request": request,
                                                        "title": "code 403",
                                                        "code": 403,
                                                        "message": "access forbidden"})
    @app.exception_handler(404)
    async def custom_404_handler(request, __):
        return templates.TemplateResponse("code.html", {"request": request,
                                                        "title": "code 404",
                                                        "code": 404,
                                                        "message": "page not found"})

    @app.exception_handler(418)
    async def custom_418_handler(request, __):
        return templates.TemplateResponse("code.html", {"request": request,
                                                        "title": "code 418",
                                                        "code": 418,
                                                        "message": "I'm a teapot"})


    @app.exception_handler(500)
    async def custom_500_handler(request, __):
        return templates.TemplateResponse("code.html", {"request": request,
                                                        "title": "code 500",
                                                        "code": 500,
                                                        "message": "internal server error"})

    @app.exception_handler(501)
    async def custom_501_handler(request, __):
        return templates.TemplateResponse("code.html", {"request": request,
                                                        "title": "code 501",
                                                        "code": 501,
                                                        "message": "not implemented"})

    @app.exception_handler(505)
    async def custom_505_handler(request, __):
        return templates.TemplateResponse("code.html", {"request": request,
                                                        "title": "code 505",
                                                        "code": 505,
                                                        "message": "http version not supported"})


async def start() -> None:
    """
    start of all processes
    :return: None
    """

    app = fastapi.FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.mount("/static", StaticFiles(directory="src/static"), name="static")

    import_routers(app)
    init_codes(app)

    config = uvicorn.Config(app=app,
                            host=settings.HOST,
                            port=settings.PORT,
                            loop="asyncio",)
    server = uvicorn.Server(config=config)
    await asyncio.gather(server.serve())


if "__main__" == __name__:
    try:
        asyncio.run(start())
    except KeyboardInterrupt:
        pass


