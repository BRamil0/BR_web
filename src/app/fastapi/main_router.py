from fastapi import APIRouter
from starlette.responses import HTMLResponse

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def get_index():
    with open("src/static/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())

@router.get("/test/")
async def root():
    return {"message": "Hello World"}