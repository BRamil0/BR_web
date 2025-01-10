"""the server startup file"""
import asyncio

import uvicorn
import fastapi
import ssl
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.staticfiles import StaticFiles

from src.config.config import settings
from src.backend.core.templates import templates

from src.backend.fastapi_app import auth_api, blog_api, api, auth, telegram, indexing, base, blog, roles_api

from src.logger.logger import logger, log_requests
from src.logger.record_log import record_log

class CustomStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope):
        response = await super().get_response(path, scope)
        if response.status_code == 404:
            return fastapi.responses.Response("File not found", status_code=404)
        if path.endswith(".js"):
            response.headers["Content-Type"] = "application/javascript"
        return response

def ssl_init() ->ssl.SSLContext:
    """

    :return:
    """
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(settings.file_ssl_cert, settings.file_ssl_key)
    return ssl_context

def import_routers(app: fastapi.FastAPI) -> None:
    """
    import routers
    :param app: fastapi.FastAPI
    :return: None
    """

    app.include_router(base.router)
    app.include_router(telegram.router)
    app.include_router(indexing.router)
    app.include_router(api.router)
    app.include_router(blog.router)
    app.include_router(blog_api.router)
    app.include_router(auth.router)
    app.include_router(auth_api.router)
    app.include_router(roles_api.router)


def init_codes(app: fastapi.FastAPI) -> None:
    """
    init codes
    :param app: fastapi.FastAPI
    :return: None
    """

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


def fast_app_start() -> fastapi.FastAPI:
    """"
    start of fastapp
    :return: fastapi.FastAPI
    """
    app: fastapi.FastAPI = fastapi.FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(BaseHTTPMiddleware, dispatch=log_requests)

    app.mount("/static", CustomStaticFiles(directory="src/frontend/static"), name="static")

    import_routers(app)
    init_codes(app)
    return app

async def start() -> None:
    """
    start the server
    :return: None
    """
    logger.opt(colors=True).info("<le><b>Server</b></le> | <lm><b>Starting server...</b></lm>")
    logger.opt(colors=True).info(f"<le><b>Server</b></le> | <lc>Https: <c><b>{settings.https}</b></c></lc> | <lc>Debug mode: <c><b>{settings.DEBUG}</b></c></lc> | <lc>Debug database mode: <c><b>{settings.DEBUG_DATABASE}</b></c></lc> | <lc>Logging: <c><b>{settings.is_log_record}</b></c></lc>")

    record_log(logger)

    app: fastapi.FastAPI = fast_app_start()

    config: uvicorn.Config = uvicorn.Config(app=app,
                                            host=settings.host,
                                            port=settings.port,
                                            loop="asyncio",
                                            reload=settings.DEBUG,
                                            log_config=None)
    if settings.https:
        config.ssl = ssl_init()
        host_ssl = "https"
    else:
        host_ssl = "http"
    server = uvicorn.Server(config=config)

    host = server.config.host
    if host not in f"{host_ssl}://":
        host = f"{host_ssl}://{host}"
    logger.opt(colors=True).info(f"<le><b>Server</b></le> | <lc>The server is running at: <c><b>{host}:{server.config.port}</b></c></lc> <ly><v>(press ctrl+c to stop)</v></ly>")

    new_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(new_loop)

    try:
        await server.serve()
    finally:
        new_loop.close()

if "__main__" == __name__:
    try:
        asyncio.run(start())
    except KeyboardInterrupt:
        logger.opt(colors=True).info("<le><b>Server</b></le> | <e><b>Server shutdown by user.</b></e>")
    except BaseException as e:
        logger.opt(colors=True).critical(f"<le><b>Server</b></le> | <e><b>The server has been shut down due to a critical error or unhandled exception, for more details: {e}</b></e>")
        raise e