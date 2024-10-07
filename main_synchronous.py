import asyncio

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

def start() -> None:
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

    config = uvicorn.Config(app=app,
                            host=settings.HOST,
                            port=settings.PORT,
                            reload=True,
                            log_level="info",)
    server = uvicorn.Server(config=config)

    asyncio.run(server.serve())


if "__main__" == __name__:
    try:
        start()
    except KeyboardInterrupt:
        pass