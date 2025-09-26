from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Загружаем .env
load_dotenv(override=True)

class Settings(BaseSettings):
    # Debug
    debug: bool

    # PostgreSQL
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str

    # Новый параметр: включение корневого эндпоинта
    root_endpoint: int

    # Версия CMS
    CMS_VERSION: str

    # JWT настройки
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"
        extra = "ignore"  # Игнорировать лишние переменные
        validate_assignment = True  # проверка типов при присвоении

# Функция для создания объекта Settings с актуальным .env
def get_settings() -> Settings:
    load_dotenv(override=True)
    return Settings()

# Изначальный объект настроек
settings = get_settings()

# Лог версии при старте
print(f"CubeNet CMS версия: {settings.CMS_VERSION}")
