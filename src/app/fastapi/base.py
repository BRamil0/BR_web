from fastapi import APIRouter
from starlette import status
from starlette.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

router = APIRouter(
    tags=["base"],
)
templates = Jinja2Templates(directory="src/templates")



@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request,
                                                     "title": "Головна",
                                                     "link": "index"})

@router.get("/index")
async def home():
    return RedirectResponse(url="/")

@router.get("/terms_of_use", response_class=HTMLResponse)
async def terms_of_use(request: Request):
    return templates.TemplateResponse("terms_of_use.html", {"request": request,
                                                            "title": "Умови використання",
                                                            "link": "terms_of_use"})

@router.get("/privacy_policy", response_class=HTMLResponse)
async def privacy_policy(request: Request):
    return templates.TemplateResponse("privacy_policy.html", {"request": request,
                                                              "title": "Політика конфіденційності",
                                                              "link": "privacy_policy"})

@router.get("/cookie_policy", response_class=HTMLResponse)
async def cookie_policy(request: Request):
    return templates.TemplateResponse("cookie_policy.html", {"request": request,
                                                             "title": "Політика використання cookie",
                                                             "link": "cookie_policy"})

@router.get("/content_used", response_class=HTMLResponse)
async def content_used(request: Request):
    return templates.TemplateResponse("content_used.html", {"request": request,
                                                            "title": "Використаний контент",
                                                            "link": "content_used"})

@router.get("/contact", response_class=HTMLResponse)
async def contact(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request,
                                                       "title": "Контакти",
                                                       "link": "contact"})

@router.get("/project", response_class=HTMLResponse)
async def project(request: Request):
    return templates.TemplateResponse("project.html", {"request": request,
                                                       "title": "Мої проєкти",
                                                       "link": "project"})

@router.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request,
                                                     "title": "Про мене",
                                                     "link": "about"})

@router.get("/418", status_code=status.HTTP_418_IM_A_TEAPOT)
async def code_418(request: Request):
    return templates.TemplateResponse("code.html", {"request": request,
                                                    "title": "code 418",
                                                    "code": 418,
                                                    "message": "I'm a teapot",
                                                    "link": "418"})