from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel
from engine.api.public.auth.logic import create_access_token, get_current_user, register_user, authenticate_user
from engine.core.database.models import User
from engine.core.database.database import get_db
from engine.core.config.config import settings
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/auth", tags=["auth"])
limiter = Limiter(key_func=get_remote_address)

# Pydantic schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str
    password_again: str

class TokenRequest(BaseModel):
    token: str

class MessageResponse(BaseModel):
    message: str

class UserInDB(BaseModel):
    id: int
    uuid: str
    username: str
    email: str
    role: str
    ip: str | None
    hd: bool
    money: float
    created_at: str | None
    last_login: str | None
    activate_token: str | None
    is_activate: bool

# Endpoints
@router.post("/register", response_model=MessageResponse)
@limiter.limit("2/minute")
async def register(
    request: Request,
    form_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    user = await register_user(db, form_data.username, form_data.email, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Username or email already exists")
    return {"message": "User registered successfully"}

@router.post("/login", response_model=Token)
@limiter.limit("2/minute")
async def login(
    request: Request,
    form_data: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    if form_data.password != form_data.password_again:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match",
        )
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/about_me", response_model=UserInDB)
@limiter.limit("40/minute")
async def about_me(
    request: Request,
    token_data: TokenRequest,
    db: AsyncSession = Depends(get_db)
):
    current_user = await get_current_user(token_data.token, db)
    return UserInDB(
        id=current_user.id,
        uuid=str(current_user.uuid),
        username=current_user.username,
        email=current_user.email,
        role=current_user.role,
        ip=str(current_user.ip) if current_user.ip else None,
        hd=current_user.hd,
        money=float(current_user.money),
        created_at=current_user.created_at.isoformat() if current_user.created_at else None,
        last_login=current_user.last_login.isoformat() if current_user.last_login else None,
        activate_token=current_user.activate_token,
        is_activate=current_user.is_activate
    )

@router.post("/refresh_token", response_model=Token)
@limiter.limit("2/minute")
async def refresh_token(
    request: Request,
    token_data: TokenRequest,
    db: AsyncSession = Depends(get_db)
):
    current_user = await get_current_user(token_data.token, db)
    access_token = create_access_token(data={"sub": current_user.username}, expires_days=7)
    return {"access_token": access_token, "token_type": "bearer"}