from datetime import datetime

from fastapi import APIRouter, status, Request
from starlette.responses import HTMLResponse, RedirectResponse

from src.backend.core.router_config import templates

router = APIRouter(
    tags=["base"],
)


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request, "index.html", { 
                                                     "title": "Головна",
                                                     "link": "index",
                                                     "description": "Домашня сторінка",})

@router.get("/index")
async def home():
    return RedirectResponse(url="/")

@router.get("/site_map", response_class=HTMLResponse)
async def site_map(request: Request):
    return templates.TemplateResponse(request, "site_map.html", { 
                                                        "title": "Карта сайту",
                                                        "link": "site_map",
                                                        "description": "Список всіх доступних сторінок",})


@router.get("/terms_of_use", response_class=HTMLResponse)
async def terms_of_use(request: Request):
    return templates.TemplateResponse(request, "terms_of_use.html", { 
                                                            "title": "Умови використання",
                                                            "link": "terms_of_use",
                                                            "description": "Умови використання сайту",})

@router.get("/privacy_policy", response_class=HTMLResponse)
async def privacy_policy(request: Request):
    return templates.TemplateResponse(request, "privacy_policy.html", { 
                                                              "title": "Політика конфіденційності",
                                                              "link": "privacy_policy",
                                                              "description": "Інформація про вашу конфіденційність",})

@router.get("/cookie_policy", response_class=HTMLResponse)
async def cookie_policy(request: Request):
    return templates.TemplateResponse(request, "cookie_policy.html", { 
                                                             "title": "Політика використання cookie",
                                                             "link": "cookie_policy",
                                                             "description": "Інформація про використання cookie",})

@router.get("/content_used", response_class=HTMLResponse)
async def content_used(request: Request):
    return templates.TemplateResponse(request, "content_used.html", { 
                                                            "title": "Використаний контент",
                                                            "link": "content_used",
                                                            "description": "Список всіх джерел з якими ми використовуємо контент",})

@router.get("/contact", response_class=HTMLResponse)
async def contact(request: Request):
    return templates.TemplateResponse(request, "contact.html", { 
                                                       "title": "Контакти",
                                                       "link": "contact",
                                                       "description": "Контактні дані",})

@router.get("/project", response_class=HTMLResponse)
async def project(request: Request):
    return templates.TemplateResponse(request, "project.html", { 
                                                       "title": "Мої проєкти",
                                                       "link": "project",
                                                       "description": "Список моїх проєктів",})

@router.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    birth_date = datetime(2006, 10, 23)
    current_date = datetime.now()
    years_old = current_date.year - birth_date.year - ((current_date.month, current_date.day) < (birth_date.month, birth_date.day))
    return templates.TemplateResponse(request, "about.html", { 
                                                     "title": "Про мене",
                                                     "link": "about",
                                                     "description": "Інформація про автора сайту",
                                                     "years_old": years_old,})

@router.get("/about_site", response_class=HTMLResponse)
async def about_site(request: Request):
    return templates.TemplateResponse(request, "about_site.html", { 
                                                          "title": "about_site",
                                                          "link": "about_site",
                                                          "description": "Інформація про сайт",})

@router.get("/418", status_code=status.HTTP_418_IM_A_TEAPOT)
async def code_418(request: Request):
    return templates.TemplateResponse(request, "code.html", { 
                                                    "title": "code 418",
                                                    "code": 418,
                                                    "message": "I'm a teapot",
                                                    "description": "code 418",
                                                    "link": "418"})