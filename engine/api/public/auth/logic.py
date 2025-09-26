from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends
from engine.core.database.models import User
from engine.core.database.database import get_item_by_field, create_item, get_db
from engine.core.config.config import settings
import bcrypt

async def register_user(db: AsyncSession, username: str, email: str, password: str):
    """
    Registers a user. Returns None if username/email already exists.
    """
    if await get_item_by_field(db, User, "username", username) or await get_item_by_field(db, User, "email", email):
        return None
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    user = User(username=username, email=email, password_hash=hashed_password)
    return await create_item(db, user)

async def authenticate_user(db: AsyncSession, username: str, password: str):
    """
    Authenticates a user. Returns None if authentication fails.
    """
    user = await get_item_by_field(db, User, "username", username)
    if not user or not bcrypt.checkpw(password.encode("utf-8"), user.password_hash.encode("utf-8")):
        return None
    return user

def create_access_token(data: dict, expires_days: int = None):
    """
    Creates a JWT token based on provided data.
    """
    to_encode = data.copy()
    if expires_days:
        expire = datetime.utcnow() + timedelta(days=expires_days)
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str, db: AsyncSession):
    """
    Returns the current user based on the token.
    Raises 401 if token is invalid or user not found.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await get_item_by_field(db, User, "username", username)
    if user is None:
        raise credentials_exception
    return user