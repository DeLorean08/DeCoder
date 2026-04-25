from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
import redis.asyncio as redis
from app.core.config import settings

redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    decode_responses=True
)

async_engine = create_async_engine(settings.database_url_async, echo=True)
AsyncSessionFactory = async_sessionmaker(
bind=async_engine,
expire_on_commit=False,
class_=AsyncSession
)