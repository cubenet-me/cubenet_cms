from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# Загружаем .env
load_dotenv(override=True)

class Settings(BaseSettings):
    # Debug
    debug: bool = True

    # PostgreSQL
    POSTGRES_USER: str = "user"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "cubenet"
    POSTGRES_HOST: str = "db"

    # Новый параметр: включение корневого эндпоинта
    root_endpoint: int = 1  # 1 = включен, 0 = выключен

    class Config:
        env_file = ".env"
        extra = "ignore"  # Игнорировать лишние переменные окружения

# Функция для создания нового объекта Settings с актуальным .env
def get_settings():
    load_dotenv(override=True)
    return Settings()

# Изначальный объект настроек
settings = get_settings()
