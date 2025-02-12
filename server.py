"""the server startup file"""
import asyncio

import uvicorn
import fastapi
import slowapi
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.staticfiles import StaticFiles
from slowapi.errors import RateLimitExceeded

from src.config.config import settings
from src.backend.core.router_config import templates, limiter

from src.backend.fastapi_app import auth_api, blog_api, api, auth, telegram, indexing, base, blog, roles_api

from src.logger.logger import logger, log_requests
from src.logger.record_log import record_log

def configure_app(app: fastapi.FastAPI) -> None:
    """Configures the FastAPI application."""

    # Register routers
    app.include_router(base.router)
    app.include_router(telegram.router)
    app.include_router(indexing.router)
    app.include_router(api.router)
    app.include_router(blog.router)
    app.include_router(blog_api.router)
    app.include_router(auth.router)
    app.include_router(auth_api.router)
    app.include_router(roles_api.router)

    # Define error handlers
    error_handlers = {
        403: ("Code 403", "Access forbidden"),
        404: ("Code 404", "Page not found"),
        418: ("Code 418", "I'm a teapot"),
        500: ("Code 500", "Internal server error"),
        501: ("Code 501", "Not implemented"),
        505: ("Code 505", "HTTP version not supported"),
    }

    def create_error_handler(error_status_code: int, error_title: str, error_message: str):
        async def error_handler(request, __):
            return templates.TemplateResponse(
                "code.html", {"request": request, "title": error_title, "code": error_status_code, "message": error_message}
            )
        return error_handler

    for status_code, (title, message) in error_handlers.items():
        app.add_exception_handler(status_code, create_error_handler(status_code, title, message))

def create_fastapi_app() -> fastapi.FastAPI:
    """
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

    app.mount("/static", StaticFiles(directory="src/frontend/static"), name="static")
    app.add_exception_handler(RateLimitExceeded, slowapi._rate_limit_exceeded_handler) # type: ignore
    app.state.limiter = limiter # type: ignore
    configure_app(app)
    return app

async def start() -> None:
    """
    start the server
    :return: None
    """
    logger.opt(colors=True).info("<le><b>Server</b></le> | <lm><b>Starting server...</b></lm>")
    logger.opt(colors=True).info(f"<le><b>Server</b></le> | <lc>Version: <c><b>{settings.server_version}</b></c></lc> | <lc>Version API: <c><b>{settings.api_version}</b></c></lc>")
    logger.opt(colors=True).info(f"<le><b>Server</b></le> | <lc>Https: <c><b>{settings.https}</b></c></lc> | <lc>Debug mode: <c><b>{settings.DEBUG}</b></c></lc> | <lc>Debug database mode: <c><b>{settings.DEBUG_DATABASE}</b></c></lc> | <lc>Log entry: <c><b>{settings.is_log_record}</b></c></lc> | <lc>Experimental: <c><b>{settings.experimental_functions}</b></c></lc>")

    record_log(logger)

    app: fastapi.FastAPI = create_fastapi_app()

    config: uvicorn.Config = uvicorn.Config(app=app,
                                            host=settings.host,
                                            port=settings.port,
                                            loop="asyncio",
                                            reload=settings.DEBUG,
                                            log_config=None,)
    if settings.https:
        config.ssl_keyfile = settings.file_ssl_key
        config.ssl_certfile = settings.file_ssl_cert
        host_ssl = "https"
    else:
        host_ssl = "http"

    server = uvicorn.Server(config=config)
    host = server.config.host
    if not host.startswith(f"{host_ssl}://"):
        host = f"{host_ssl}://{host}"
    logger.opt(colors=True).info(f"<le><b>Server</b></le> | <lc>The server is running at: <c><b>{host}:{server.config.port}</b></c></lc> <ly><v>(press ctrl+c to stop)</v></ly>")

    await server.serve()

if "__main__" == __name__:
    try:
        asyncio.run(start())
    except KeyboardInterrupt:
        logger.opt(colors=True).info("<le><b>Server</b></le> | <e><b>Server shutdown by user.</b></e>")
    except Exception as e:
        logger.opt(colors=True).critical(f"<le><b>Server</b></le> | <e><b>The server has been shut down due to a critical error or unhandled exception, for more details: {e}</b></e>")
        raise e