from fastapi import APIRouter, Depends
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

# Правильные импорты
from engine.core.database.database import get_db
from engine.core.database.models import User  

router = APIRouter(prefix="/testing_db", tags=["testing_db"])  # Категория testing_db

@router.get("/")
def example_endpoint():
    """
    Пустой эндпоинт в категории 'testing_db'.
    """
    return {"message": "Этот эндпоинт пока пустой"}

@router.get("/users")
async def get_all_users(db: AsyncSession = Depends(get_db)):
    """
    Выводит всех пользователей из таблицы User.
    """
    result = await db.execute(select(User))
    users = result.scalars().all()
    return [{"id": u.id, "username": u.username, "email": u.email, "role": u.role} for u in users]

@router.get("/users_raw")
async def get_users_raw(db: AsyncSession = Depends(get_db)):
    """
    Выводит всех пользователей как 'сырой' словарь через SQL.
    """
    result = await db.execute(text("SELECT * FROM users"))
    rows = result.mappings().all()
    return rows

# Ни в коем случае не создаём FastAPI() здесь
# Подключение делаем через loader:
# from engine.main import app
# app.include_router(router)
