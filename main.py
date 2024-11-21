"""the main application startup file"""
import asyncio
import subprocess
import signal

import uvicorn
import fastapi
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.staticfiles import StaticFiles

from src.config.config import settings
from src.backend.templates import templates

from src.fastapi_app import auth_api, blog_api, api, auth, telegram, indexing, base, blog

from src.logger.logger import logger, log_requests
from src.logger.record_log import record_log

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

    app.mount("/static", StaticFiles(directory="src/static"), name="static")

    import_routers(app)
    init_codes(app)
    return app


async def run_npm() -> bool:
    if settings.DEBUG:
        logger.opt(colors=True).info("<e>Frontend</e> | <e><b>Watching frontend...</b></e>")
        return await run_command("npm run watch")
    else:
        logger.opt(colors=True).info("<e>Frontend</e> | <e><b>Building frontend...</b></e>")
        return await run_command("npm run build")


async def run_command(command: str) -> bool:
    """run command"""
    logger.opt(colors=True).info(f"<e>Frontend</e> | <c>Starting command: <b>{command}</b></c>")
    process = await asyncio.create_subprocess_shell(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    async def read_stdout():
        try:
            while True:
                line = await process.stdout.readline()
                if not line:
                    break
                decoded_line = line.decode('utf-8').strip()
                if decoded_line:
                    logger.opt(colors=True).info(f"<e>Frontend</e> | <c><b>stdout</b></c> | {line.decode('utf-8').strip()}")
        except Exception as error:
            logger.opt(colors=True).error(f"<e>Frontend</e> | <c><b>stdout read error: {str(error)}</b></c>")

    async def read_stderr():
        try:
            while True:
                line = await process.stderr.readline()
                if not line:
                    break
                decoded_line = line.decode('utf-8').strip()
                if decoded_line:
                    logger.opt(colors=True).error(f"<e>Frontend</e> | <c><b>stderr</b></c> | {line.decode('utf-8').strip()}")
        except Exception as error:
            logger.opt(colors=True).error(f"<e>Frontend</e> | <c><b>stderr read error: {str(error)}</b></c>")

    try:
        await asyncio.gather(read_stdout(), read_stderr())
    except (asyncio.CancelledError, ValueError):
        logger.opt(colors=True).info("<e>Frontend</e> | <c>Attempting to stop the server process...</c>")
        process.send_signal(signal.SIGINT)
        await asyncio.sleep(2)
        process.kill()
        await process.wait()

    finally:
        if not process.returncode:
            process.send_signal(signal.SIGINT)
            await asyncio.sleep(2)
            process.kill()
            await process.wait()

    logger.opt(colors=True).info(f"<e>Frontend</e> | <c>Process exited with code <b>{process.returncode}</b></c>")
    return True

async def start() -> None:
    """
    start of all processes
    :return: None
    """
    record_log(logger)

    app: fastapi.FastAPI = fast_app_start()

    config: uvicorn.Config = uvicorn.Config(app=app,
                                            host=settings.host,
                                            port=settings.port,
                                            loop="asyncio",
                                            reload=settings.DEBUG,
                                            log_config=None)
    server = uvicorn.Server(config=config)

    host = server.config.host
    if host not in "http://":
        host = f"http://{host}"
    logger.opt(colors=True).info(f"<e>Server</e> | <c>The server is running at: <b>{host}:{server.config.port}</b></c> <y>(press ctrl+c to stop)</y>")

    new_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(new_loop)

    try:
        await asyncio.gather(run_npm(), server.serve())
    finally:
        new_loop.close()

if "__main__" == __name__:
    try:
        logger.opt(colors=True).info("<e>Server</e> | <e><b>Starting server...</b></e>")
        logger.opt(colors=True).info(f"<e>Server</e> | <cyan>Debug mode: <b>{settings.DEBUG}</b></cyan> | <cyan>Debug database mode: <b>{settings.DEBUG_DATABASE}</b></cyan> | <cyan>Logging: <b>{settings.is_log_record}</b></cyan>")
        asyncio.run(start())
    except KeyboardInterrupt:
        logger.opt(colors=True).info("<e>Server</e> | <e><b>Server shutdown by user.</b></e>")
    except BaseException as e:
        logger.opt(colors=True).critical(f"<e>Server</e> | <e><b>The server has been shut down due to a critical error or unhandled exception, for more details: {e}</b></e>")
        raise e