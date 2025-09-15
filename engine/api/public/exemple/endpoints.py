# engine/api/public/example/endpoints.py
from fastapi import APIRouter

router = APIRouter(prefix="/example", tags=["example"])  # tags будет автоматически "example"

@router.get("/endpoint")
def example_endpoint():
    # Теперь можно использовать logic, если он есть
    if "logic" in globals():
        result = logic.some_function()  # берём функцию из logic.py
        return {"message": "Результат из логики", "result": result}
    return {"message": "Этот эндпоинт пока пустой"}
