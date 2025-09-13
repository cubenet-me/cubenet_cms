# engine/api/public/db/endpoints.py
from fastapi import APIRouter
from engine.api.public.db.connection import SessionLocal
from engine.api.public.db.models.user import User

router = APIRouter()

@router.get("/db/users")
def get_users():
    db = SessionLocal()
    users = db.query(User).all()
    db.close()
    return users
