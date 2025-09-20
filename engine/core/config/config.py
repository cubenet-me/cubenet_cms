# engine/core/config/config.py
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

class Settings(BaseSettings):
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 60
    debug: bool = True

    class Config:
        env_file = ".env"
        extra = "ignore"  # Игнорировать лишние переменные окружения

# Функция для создания нового объекта Settings с актуальным .env
def get_settings():
    # Перезагружаем переменные окружения из .env
    load_dotenv(override=True)
    return Settings()

# Изначальный объект настроек
settings = get_settings()
