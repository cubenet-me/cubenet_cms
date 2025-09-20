from .database import engine, Base, get_db
from .models import User

__all__ = ["engine", "Base", "get_db", "User"]

def setup(app):
    from engine.core.logger.logger import logger
    logger.info("Инициализация модуля database...")
    Base.metadata.create_all(bind=engine)