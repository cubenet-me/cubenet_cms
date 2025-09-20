from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from engine.core.config.config import get_settings
from engine.core.logger.logger import logger

settings = get_settings()

# Формирование URL подключения к базе данных
DATABASE_URL = settings.database_url if hasattr(settings, "database_url") else "DATABASE_URL = "postgresql+asyncpg://user:password@db:5432/cubenet"

# Создание асинхронного движка
engine = create_async_engine(
    DATABASE_URL,
    echo=settings.debug,
    future=True
)

# Создание фабрики сессий
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Базовый класс для моделей
class Base(DeclarativeBase):
    pass

# Асинхронный контекстный менеджер для сессий
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()