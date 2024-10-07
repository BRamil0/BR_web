import fastapi
from fastapi.staticfiles import StaticFiles
from src.app.fastapi import main_router


def import_routers(app: fastapi.FastAPI) -> None:
    """
    import routers
    :param app: fastapi.FastAPI
    :return: None
    """
    app.include_router(main_router.router)


app = fastapi.FastAPI()

app.mount("/static", StaticFiles(directory="src/static"), name="static")

import_routers(app)
