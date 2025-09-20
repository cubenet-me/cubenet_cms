from fastapi import APIRouter

router = APIRouter(prefix="/launcher", tags=["launcher"])  # Категория launcher

@router.get("/")
def example_endpoint():
    """
    Пустой эндпоинт в категории 'launcher'.
    """
    return {"message": "Этот эндпоинт пока пустой"}

# Ни в коем случае не создаём здесь FastAPI()
# Подключение делаем через loader:
# from engine.main import app
# app.include_router(router)
