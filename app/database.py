import os

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+asyncpg://user:password@db:5432/finapi_db"
)

engine = create_async_engine(DATABASE_URL)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


async def get_db():
    """Генератор асинхронных сессий БД."""
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
