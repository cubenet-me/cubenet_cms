from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from engine.core.config.config import settings  # глобальный объект настроек

# ----------------------------
# Базовый класс для моделей
# ----------------------------
class Base(DeclarativeBase):
    pass

# ----------------------------
# Настройки базы данных
# ----------------------------
DATABASE_URL = f"postgresql+asyncpg://{settings.POSTGRES_USER}:" \
               f"{settings.POSTGRES_PASSWORD}@" \
               f"{settings.POSTGRES_HOST}:5432/" \
               f"{settings.POSTGRES_DB}"

engine = create_async_engine(
    DATABASE_URL,
    echo=settings.debug,
    future=True
)

AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# ----------------------------
# Асинхронный контекстный менеджер для сессий
# ----------------------------
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# ----------------------------
# Инициализация базы данных (создание таблиц)
# ----------------------------
async def init_db():
    from . import models  # импорт всех моделей перед созданием таблиц
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
