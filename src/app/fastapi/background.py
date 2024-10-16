import random

from fastapi import APIRouter
from fastapi.templating import Jinja2Templates

router: APIRouter = APIRouter()
templates: Jinja2Templates = Jinja2Templates(directory="src/templates")

not_use: list[int] = [2, 10, 12, 15]

@router.get("/background")
async def background():
    while True:
        ran: list[int] = random.randint(1, 20)
        if int(ran) not in not_use:
            break

    return {"image4k": f"/static/image/background/jpg/{ran}.jpg",
            "image2k": f"/static/image/background/2k/{ran}.webp",
            "image1k": f"/static/image/background/1k/{ran}.webp",}
