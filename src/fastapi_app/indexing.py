from fastapi import APIRouter
from starlette.responses import FileResponse

router = APIRouter(
    tags=["indexing"],
)


@router.get("static/robots.txt", include_in_schema=False)
async def robots():
    return FileResponse("src/static/robots.txt")


@router.get("static/sitemap.xml", include_in_schema=False)
async def sitemap():
    return FileResponse("src/static/sitemap.xml")