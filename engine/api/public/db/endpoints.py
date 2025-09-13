# engine/api/public/db/endpoints.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from engine.api.public.db.connection import SessionLocal
from engine.api.public.db.models import User  # Импорт из models.py

router = APIRouter(prefix="/db")

# Зависимость для сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users
