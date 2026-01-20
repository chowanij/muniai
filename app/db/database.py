"""
Połączenie z bazą danych - async SQLAlchemy.
"""

from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


# Engine - połączenie z bazą
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,  # Loguj SQL w trybie debug
    pool_size=settings.db_pool_size,
    max_overflow=settings.db_max_overflow,
)

# Fabryka sesji
async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# Bazowa klasa dla modeli
class Base(DeclarativeBase):
    pass


# Dependency dla FastAPI
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


# Type alias - użycie: db: DbSession
DbSession = Annotated[AsyncSession, Depends(get_db)]


# Lifecycle hooks
async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    await engine.dispose()