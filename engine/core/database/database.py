# engine/core/database/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import select, update, delete
from engine.core.config.config import settings  # глобальный объект настроек
from typing import TypeVar, Type, Optional
from uuid import UUID

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

# ----------------------------
# Универсальные CRUD-операции
# ----------------------------
T = TypeVar("T", bound=Base)

async def create_item(session: AsyncSession, item: T) -> T:
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item

async def get_item(session: AsyncSession, model: Type[T], item_id: int | UUID) -> Optional[T]:
    query = select(model).where(model.id == item_id if hasattr(model, 'id') else model.uuid == item_id)
    result = await session.execute(query)
    return result.scalar_one_or_none()

async def get_item_by_field(session: AsyncSession, model: Type[T], field: str, value: any) -> Optional[T]:
    query = select(model).where(getattr(model, field) == value)
    result = await session.execute(query)
    return result.scalar_one_or_none()

async def update_item(session: AsyncSession, model: Type[T], item_id: int | UUID, **kwargs) -> Optional[T]:
    query = update(model).where(model.id == item_id if hasattr(model, 'id') else model.uuid == item_id).values(**kwargs)
    await session.execute(query)
    await session.commit()
    return await get_item(session, model, item_id)

async def delete_item(session: AsyncSession, model: Type[T], item_id: int | UUID) -> bool:
    query = delete(model).where(model.id == item_id if hasattr(model, 'id') else model.uuid == item_id)
    result = await session.execute(query)
    await session.commit()
    return result.rowcount > 0