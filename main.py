import asyncio
import os

import uvicorn
import fastapi
from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from src.config.config import settings

from src.app.fastapi import main_router

def import_routers(app: fastapi.FastAPI) -> None:
    """
    import routers
    :param app: fastapi.FastAPI
    :return: None
    """
    app.include_router(main_router.router)

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
    print(os.path.join(os.path.dirname(__file__), "src/static/"))
    app.mount("/static", StaticFiles(directory="src/static"), name="static")

    import_routers(app)

    config = uvicorn.Config(app=app,
                            host=settings.HOST,
                            port=settings.PORT,
                            loop="asyncio")
    server = uvicorn.Server(config=config)
    await asyncio.gather(server.serve())


if "__main__" == __name__:
    try:
        asyncio.run(start())
    except KeyboardInterrupt:
        pass