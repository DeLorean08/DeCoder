import time
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from app.dependencies import get_db
from sqlalchemy.ext.asyncio import  AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.shemas.token import Token
from app.shemas.user import UserCreate, UserLogin
from pathlib import Path
from app.core.security import hash_password, verify_password, encode_jwt
from uuid import uuid4
from fastapi.templating import Jinja2Templates
from app.core.logging_config import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["AUTH"])

template_dir = Path(__file__).parent.parent.parent.parent / "frontend" / "templates"
templates = Jinja2Templates(directory=template_dir)

@router.get("/register", response_class=HTMLResponse)
async def get_register_page(request: Request):
    return templates.TemplateResponse(request=request, name="register.html", context={"request": request})

@router.get("/login", response_class=HTMLResponse)
async def get_login_page(request: Request):
    return templates.TemplateResponse(request=request, name="login.html", context={"request": request})



@router.post("/register_user", status_code=200)
async def create_user(user: UserCreate = Depends(UserCreate.as_form),
    db: AsyncSession = Depends(get_db)):

    start_time = time.perf_counter()
    logger.debug(f"Попытка регистрации пользователя: {user.email}")
    result =  await db.execute(select(User).where(User.email == user.email))
    data = result.scalar_one_or_none()

    if data:
        logger.warning(
            f"Registration failed: email already exists", 
            extra={"email": user.email, "reason": "duplicate_email"}
        )
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Этот Email уже зарегистрирован")
        
    hashed_password = hash_password(user.password)

    try:
        new_id = uuid4()
        new_user = User(
            id = new_id,
            name = user.name,
            email = user.email,
            hashed_password = hashed_password
        )

        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        process_time = time.perf_counter() - start_time

        logger.info(
            f"User created successfully: {user.email}",
            extra={
                "user_id": str(new_id),
                "email": user.email,
                "latency": round(process_time, 4),
                "action": "user_registration"
            }
        )
        return RedirectResponse(url="/auth/login", status_code=303)
    
    except Exception as e:
        await db.rollback()
        logger.error(
            f"Database error during registration for {user.email}: {e}", 
            exc_info=True,
            extra={"email": user.email}
        )
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка базы данных!")
   
    

async def login_user(
    user: UserLogin = Depends(UserLogin.as_form),
    db: AsyncSession = Depends(get_db)):
    
    logger.debug(f"Попытка входа пользователя: {user.email}")
    result =  await db.execute(select(User).where(User.email == user.email))
    login_data = result.scalar_one_or_none()

    if not login_data:
        logger.warning(
            f"Login failed: email or password not correct", 
            extra={"email": user.email, "reason": "email_or_password_not_correct"}
        )
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email or password not correct")

    valid_login = verify_password(user.password, login_data.hashed_password)

    if not valid_login:
        logger.warning(
            f"Login failed: email or password not correct", 
            extra={"email": user.email, "reason": "email_or_password_not_correct"}
        )
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email or password not correct")
    
    return login_data


@router.post("/login_user", response_model=Token)
def auth_user_issue_jwt(
    response: Response,
    user: User = Depends(login_user),
):
    jwt_payload = {
        "sub": str(user.id),
        "name": user.name,
        "email": user.email
    }
    
    token = encode_jwt(jwt_payload)
    response = RedirectResponse(url="/user/home", status_code=303)

    response.set_cookie(
        key="access_token", 
        value=token, 
        httponly=True,   
        max_age=3600,
        samesite="lax"   
    )

    return response