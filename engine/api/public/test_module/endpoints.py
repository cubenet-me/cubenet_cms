from fastapi import APIRouter
from .logic import get_test_message

router = APIRouter(prefix="/test", tags=["test"])

@router.get("/")
async def test_root():
    return get_test_message()

@router.get("/{name}")
async def test_with_name(name: str):
    return {"message": f"Hello, {name}!"}
