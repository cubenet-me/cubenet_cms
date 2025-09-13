from fastapi import APIRouter, FastAPI

app = FastAPI()
router = APIRouter(prefix="/launcher", tags=["launcher"])  # Категория example

# Пустой эндпоинт в категории example
@router.get("/")
def example_endpoint():
    """
    Пустой эндпоинт в категории 'launcher'.
    """
    return {"message": "Этот эндпоинт пока пустой"}

# Подключаем роутер к приложению
app.include_router(router)
