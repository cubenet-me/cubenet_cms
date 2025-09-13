from fastapi import APIRouter, FastAPI

app = FastAPI()
router = APIRouter(prefix="/example", tags=["example"])  # Категория example

# Пустой эндпоинт в категории example
@router.get("/endpoint")
def example_endpoint():
    """
    Пустой эндпоинт в категории 'example'.
    """
    return {"message": "Этот эндпоинт пока пустой"}

# Подключаем роутер к приложению
app.include_router(router)
