"""this file is needed only for vercel, do not run it, instead it is better to run it through ‘main.py’"""

import fastapi
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.app.fastapi import base

def import_routers(app: fastapi.FastAPI) -> None:
    """
    import routers
    :param app: fastapi.FastAPI
    :return: None
    """
    app.include_router(base.router)

templates = Jinja2Templates(directory="src/templates")

app = fastapi.FastAPI()

app.mount("/static", StaticFiles(directory="src/static"), name="static")

import_routers(app)


@app.exception_handler(404)
async def custom_404_handler(request, __):
    return templates.TemplateResponse("code.html", {"request": request,
                                                    "title": "code 404",
                                                    "code": 404,
                                                    "message": "page not found"})
