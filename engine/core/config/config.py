# engine/core/config/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    private_api_token: str
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 60
    debug: bool = True

    class Config:
        env_file = ".env"

settings = Settings()