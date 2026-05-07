import time
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from app.dependencies import get_current_user
from sqlalchemy import select
from app.shemas.user import UserOut
from pathlib import Path
from uuid import uuid4
from fastapi.templating import Jinja2Templates
from app.core.logging_config import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/problem", tags=["PROBLEM"])

template_dir = Path(__file__).parent.parent.parent.parent / "frontend" / "templates"
templates = Jinja2Templates(directory=template_dir)

@router.get("/", response_class=HTMLResponse)
async def get_home_page(request: Request, user: UserOut = Depends(get_current_user)):
    return templates.TemplateResponse(request=request, name="problems.html", context={"request": request, "user": user})