from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencies import get_db
from sqlalchemy.ext.asyncio import  AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.shemas.user import UserCreate
from app.core.security import hash_password
from uuid import uuid4
import logging

router = APIRouter(prefix="/auth", tags=["AUTH"])

@router.post("/register", status_code=201)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    result =  await db.execute(select(User).where(User.email == user.email))
    data = result.scalar_one_or_none()

    if data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Этот Email уже зарегистрирован")
    
    hashed_password = hash_password(user.password)

    try:
        new_user = User(
            id = uuid4(),
            name = user.name,
            email = user.email,
            hashed_password = hashed_password
        )

        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        return {"message": "Регистрация успешно прошла!"}
    
    except Exception as e:
        await db.rollback()
        print(f"Database error: {e}") 
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка базы данных!")
    
