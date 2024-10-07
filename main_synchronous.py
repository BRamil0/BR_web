import uvicorn
import fastapi
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

    app.mount("/static", StaticFiles(directory="src/static"), name="static")

    import_routers(app)

    uvicorn.run(app=app,
                host=settings.HOST,
                port=settings.PORT,)

if "__main__" == __name__:
    try:
        start()
    except KeyboardInterrupt:
        pass