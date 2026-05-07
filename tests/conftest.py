import sys
import asyncio

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
import redis.asyncio as redis
from app.core.config import settings
import pytest
from app.models.base import Base
from app.main import app
from httpx import AsyncClient, ASGITransport
from app.dependencies import get_db
from typing import AsyncGenerator


redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    decode_responses=True
)

test_engine = create_async_engine(settings.test_database_url_async, echo=True)
AsyncSessionFactory = async_sessionmaker(
bind=test_engine,
expire_on_commit=False,
class_=AsyncSession
)

@pytest.fixture(scope="session", autouse=True)
async def setup_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield 
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    test_engine = create_async_engine(settings.test_database_url_async, echo=True)
    AsyncSessionFactory = async_sessionmaker(
    bind=test_engine,
    expire_on_commit=False,
    class_=AsyncSession)
    async with AsyncSessionFactory() as session:
        try:
            yield session
        finally:
            await session.rollback()

@pytest.fixture(scope="function")
async def client(db_session):
    async def override_get_db():
        yield db_session
        
    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as cl:
        yield cl
    app.dependency_overrides.clear()
