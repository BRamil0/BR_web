from fastapi import APIRouter, Request
from starlette.responses import FileResponse
from src.backend.core.router_config import limiter

router = APIRouter(
    tags=["indexing"],
)


@router.get("/robots.txt")
@limiter.limit("5/1c")
async def robots(request: Request):
    return FileResponse("src/frontend/static/robots.txt")


@router.get("/sitemap.xml")
@limiter.limit("5/1c")
async def sitemap(request: Request):
    return FileResponse("src/frontend/static/sitemap.xml")