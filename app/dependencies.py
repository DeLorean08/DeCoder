from app.database import AsyncSession, AsyncSessionFactory
from typing import AsyncGenerator
from fastapi import  Request
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import  AsyncSession
from app.core.security import decode_jwt


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionFactory() as session:
        yield session

async def get_current_user(request: Request):
    token = request.cookies.get("access_token")

    if not token:
        return None
    try:
        payload = decode_jwt(token)
        return payload
    except Exception:
        RedirectResponse(url="/", status_code=303)
