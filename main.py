"""the main application startup file"""

import asyncio

import uvicorn
import fastapi
from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from src.config.config import settings

from fastapi.templating import Jinja2Templates

from src.app.fastapi import base


def import_routers(app: fastapi.FastAPI) -> None:
    """
    import routers
    :param app: fastapi.FastAPI
    :return: None
    """
    app.include_router(base.router)


def init_codes(app: fastapi.FastAPI) -> None:
    """
    init codes
    :param app: fastapi.FastAPI
    :return: None
    """

    templates = Jinja2Templates(directory="src/templates")

    @app.exception_handler(404)
    async def custom_404_handler(request, __):
        return templates.TemplateResponse("code.html", {"request": request,
                                                        "title": "code 404",
                                                        "code": 404,
                                                        "message": "page not found"})


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


