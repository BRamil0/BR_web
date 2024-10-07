import asyncio

import uvicorn
import fastapi
from starlette.middleware.cors import CORSMiddleware
from src.config.config import settings


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
