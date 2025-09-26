from fastapi import APIRouter, Request
from engine.core.limiter import slowapi

router = APIRouter(prefix="/launcher", tags=["launcher"])  # Категория launcher

@router.get("/")
@slowapi("1/minute")
async def example_endpoint(request: Request):
    """
    Пустой эндпоинт в категории 'launcher'.
    """
    return {"message": "Этот эндпоинт пока пустой"}