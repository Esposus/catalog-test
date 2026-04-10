from collections.abc import AsyncGenerator
from datetime import UTC, datetime

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from app.core.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
Base = declarative_base()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


async def health_live():
    try:
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
        db_status = "ok"
        message = "Успешное подключение к базе данных"
    except Exception as e:
        db_status = "error"
        message = f"Не удалось подключиться к базе данных: {str(e)}"

    return {
        "status": db_status,
        "message": message,
        "timestamp": datetime.now(UTC).isoformat(),
    }
