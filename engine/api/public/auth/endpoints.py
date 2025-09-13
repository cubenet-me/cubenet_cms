# engine/api/public/auth/endpoints.py
from fastapi import APIRouter, Form
from engine.api.public.auth.logic import login_user

router = APIRouter(tags=["auth"])

@router.post("/login")
async def login(username: str = Form(...), password: str = Form(...), remember_me: bool = Form(False)):
    """
    Авторизация пользователя и выдача JWT токена.
    remember_me = True → срок жизни токена = JWT_REFRESH_EXPIRE_MINUTES
    """
    return login_user(username, password, remember_me)
