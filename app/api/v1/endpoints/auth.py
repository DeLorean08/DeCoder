import time
from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencies import get_db
from sqlalchemy.ext.asyncio import  AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.shemas.user import UserCreate
from app.core.security import hash_password
from uuid import uuid4
from app.core.logging_config import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["AUTH"])

@router.post("/register", status_code=201)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    start_time = time.perf_counter()
    logger.debug(f"Попытка регистрации пользователя: {user.email}")
    result =  await db.execute(select(User).where(User.email == user.email))
    data = result.scalar_one_or_none()
    request_db = time.perf_counter() - start_time
    print(f"DB time: {request_db}")
    if data:
        logger.warning(
            f"Registration failed: email already exists", 
            extra={"email": user.email, "reason": "duplicate_email"}
        )
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Этот Email уже зарегистрирован")
        
    hashed_start = time.perf_counter()
    hashed_password = hash_password(user.password)
    hashed_time = time.perf_counter() - hashed_start

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
                "hl": round(hashed_time, 4),
                "action": "user_registration"
            }
        )
        return {"message": "Регистрация успешно прошла!"}
    
    except Exception as e:
        await db.rollback()
        logger.error(
            f"Database error during registration for {user.email}: {e}", 
            exc_info=True,
            extra={"email": user.email}
        )
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка базы данных!")
    
