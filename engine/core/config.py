# engine/core/config.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    # PostgreSQL
    db_user: str
    db_password: str
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str

    # API tokens
    private_api_token: str

    # JWT
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 60

    # Прочие настройки
    debug: bool = True

    class Config:
        env_file = ".env"

settings = Settings()
