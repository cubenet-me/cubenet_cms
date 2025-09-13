# engine/api/public/auth/logic.py
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from engine.core.security import create_jwt_token, verify_password
from engine.api.public.db.connection import SessionLocal
from engine.api.public.db.models import User

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.nickname == username).first()
    if not user or not verify_password(password, user.password_hash):
        return None
    return user

def login_user(db: Session, username: str, password: str, remember_me: bool = False):
    user = authenticate_user(db, username, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    # Создаём JWT токен с ролью пользователя
    token = create_jwt_token({"sub": user.nickname, "role": user.role}, remember_me=remember_me)
    return {"access_token": token, "token_type": "bearer", "role": user.role}
