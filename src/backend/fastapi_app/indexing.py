from fastapi import APIRouter
from starlette.responses import FileResponse

router = APIRouter(
    tags=["indexing"],
)


@router.get("/robots.txt")
async def robots():
    return FileResponse("src/frontend/static/robots.txt")


@router.get("/sitemap.xml")
async def sitemap():
    return FileResponse("src/frontend/static/sitemap.xml")