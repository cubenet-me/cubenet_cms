# engine/database/__init__.py
from .database import engine, Base, get_db
from .models import User
from engine.core.logger.logger import logger
from sqlalchemy.exc import OperationalError

__all__ = ["engine", "Base", "get_db", "User"]

import asyncio

async def init_db():
    logger.info("Инициализация базы данных...")

    # бесконечное ожидание соединения
    while True:
        try:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            break
        except OperationalError:
            logger.warning("База данных ещё не готова, повторная попытка через 1 секунду...")
            await asyncio.sleep(1)

    logger.info("База данных готова.")

def setup(app):
    """
    Подключаем инициализацию к событию старта FastAPI.
    """
    @app.on_event("startup")
    async def on_startup():
        await init_db()
