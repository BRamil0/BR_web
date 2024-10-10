"""this file is needed only for vercel, do not run it, instead it is better to run it through ‘main.py’"""

import fastapi
from fastapi.staticfiles import StaticFiles
from src.app.fastapi import base


def import_routers(app: fastapi.FastAPI) -> None:
    """
    import routers
    :param app: fastapi.FastAPI
    :return: None
    """
    app.include_router(base.router)


app = fastapi.FastAPI()

app.mount("/static", StaticFiles(directory="src/static"), name="static")

import_routers(app)
