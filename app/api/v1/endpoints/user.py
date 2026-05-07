from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from pathlib import Path
from fastapi.templating import Jinja2Templates
from app.core.logging_config import logging
from app.dependencies import get_current_user
from app.shemas.user import UserOut

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/user", tags=["USER"])

template_dir = Path(__file__).parent.parent.parent.parent / "frontend" / "templates"
templates = Jinja2Templates(directory=template_dir)

@router.get("/home", response_class=HTMLResponse)
async def get_home_page(request: Request, user: UserOut =  Depends(get_current_user)):
    if not user:
        return RedirectResponse(url="/", status_code=303)
    return templates.TemplateResponse(request=request, name="home.html", context={"request": request, "user": user})

@router.get("/profile", response_class=HTMLResponse)
async def get_home_page(request: Request, user: UserOut =  Depends(get_current_user)):
    if not user:
        return RedirectResponse(url="/", status_code=303)
    return templates.TemplateResponse(request=request, name="profile.html", context={"request": request, "user": user})

@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/auth/login", status_code=303)
    response.delete_cookie("access_token")
    
    return response