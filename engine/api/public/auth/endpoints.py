# engine/api/public/auth/endpoints.py
from fastapi import APIRouter, Form, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from engine.api.public.auth.logic import login_user
from engine.api.public.db.connection import SessionLocal
from engine.api.public.db.models import User
from engine.core.security import get_password_hash, verify_jwt_token

router = APIRouter(tags=["auth"])

# Зависимость для подключения к БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login")
async def login(
    username: str = Form(...),
    password: str = Form(...),
    remember_me: bool = Form(False),
    db: Session = Depends(get_db)
):
    """
    Авторизация пользователя и выдача JWT токена.
    remember_me = True → срок жизни токена = JWT_REFRESH_EXPIRE_MINUTES
    """
    return login_user(db, username, password, remember_me)

@router.post("/register")
async def register(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Регистрация нового пользователя.
    """
    # Проверяем, есть ли пользователь с таким ником или email
    if db.query(User).filter((User.nickname == username) | (User.email == email)).first():
        raise HTTPException(status_code=400, detail="Username or email already registered")

    # Создаём пользователя
    new_user = User(
        nickname=username,
        email=email,
        password_hash=get_password_hash(password),
        role="user"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"msg": "User registered successfully", "user_id": new_user.id}

@router.get("/about")
def about(x_token: str = Header(...), db: Session = Depends(get_db)):
    """
    Возвращает информацию о пользователе по JWT токену.
    """
    payload = verify_jwt_token(x_token)
    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    user = db.query(User).filter(User.nickname == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "uuid": user.uuid,
        "nickname": user.nickname,
        "email": user.email,
        "role": user.role,
        "bio": user.bio,
        "created_at": user.created_at,
        "last_login": user.last_login,
        "skin_url": getattr(user, "skin_url", None),
        "cape_url": getattr(user, "cape_url", None)
    }
