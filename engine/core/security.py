# engine/core/security.py
import os
from fastapi import Depends, Header, HTTPException
from dotenv import load_dotenv
import jwt
from datetime import datetime, timedelta
import bcrypt

load_dotenv()

# -----------------------------
# Настройки безопасности
# -----------------------------
ENABLE_SWAGGER = os.getenv("ENABLE_SWAGGER", "1") == "1"
ENABLE_REDOC = os.getenv("ENABLE_REDOC", "1") == "1"
ENABLE_OPENAPI = os.getenv("ENABLE_OPENAPI", "1") == "1"

# -----------------------------
# JWT настройки через .env
# -----------------------------
SECRET_JWT_KEY = os.getenv("SECRET_JWT_KEY", "supersecret")        # ключ для подписи JWT
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")                # алгоритм подписи
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", 60))      # срок жизни токена в минутах
JWT_REFRESH_EXPIRE_MINUTES = int(os.getenv("JWT_REFRESH_EXPIRE_MINUTES", 120))  # срок жизни при "remember me"

# -----------------------------
# Пароли
# -----------------------------
def get_password_hash(password: str) -> str:
    """Хэширование пароля"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверка пароля на соответствие хэшу"""
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode())

# -----------------------------
# JWT utility
# -----------------------------
def create_jwt_token(data: dict, remember_me: bool = False):
    """
    Создание JWT токена.
    Если remember_me=True, срок жизни = JWT_REFRESH_EXPIRE_MINUTES
    """
    to_encode = data.copy()
    expire_minutes = JWT_REFRESH_EXPIRE_MINUTES if remember_me else JWT_EXPIRE_MINUTES
    expire = datetime.utcnow() + timedelta(minutes=expire_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_JWT_KEY, algorithm=JWT_ALGORITHM)

def verify_jwt_token(token: str):
    """Проверка валидности JWT"""
    try:
        payload = jwt.decode(token, SECRET_JWT_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def refresh_jwt_token(token: str, remember_me: bool = False):
    """
    Продление токена: создает новый JWT на основе старого payload
    """
    payload = verify_jwt_token(token)
    payload.pop("exp", None)  # удаляем старое поле exp
    return create_jwt_token(payload, remember_me=remember_me)

def get_current_user(x_token: str = Header(...)):
    """Dependency для FastAPI эндпоинта — извлечение данных пользователя из JWT"""
    return verify_jwt_token(x_token)
