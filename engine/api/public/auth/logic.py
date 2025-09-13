# engine/api/public/auth/logic.py
from fastapi import HTTPException
from engine.core.security import create_jwt_token
from engine.core.roles import role_manager

# Пример "базы пользователей"
FAKE_USERS_DB = {
    "alice": {"password": "alice123", "role": "admin"},
    "bob": {"password": "bob123", "role": "user"},
}

def authenticate_user(username: str, password: str):
    user = FAKE_USERS_DB.get(username)
    if not user or user["password"] != password:
        return None
    return {"username": username, "role": user["role"]}

def login_user(username: str, password: str, remember_me: bool = False):
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    # Создаём JWT токен с ролью пользователя
    token = create_jwt_token({"sub": username, "role": user["role"]}, remember_me=remember_me)
    return {"access_token": token, "token_type": "bearer", "role": user["role"]}
