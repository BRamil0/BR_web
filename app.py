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


@app.exception_handler(fastapi.HTTPException)
async def http_exception_handler(request: fastapi.Request, exc: fastapi.HTTPException):
    if exc.status_code == 404:
        return templates.TemplateResponse("codes/code.html", {"request": request})
    return await request.app.default_exception_handler(request, exc)