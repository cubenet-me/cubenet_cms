import importlib.util
from pathlib import Path
from fastapi import APIRouter, FastAPI
from engine.core.logger import logger
import os
from dotenv import load_dotenv

PUBLIC_MODULES_PATH = Path(__file__).parent / "public"

def reload_env():
    load_dotenv(override=True)  # Перезагрузка .env

def remove_public_routes(app: FastAPI, tags: list[str]):
    """Удаляет роутеры с указанными тегами"""
    app.routes[:] = [
        route for route in app.routes
        if not getattr(route, "tags", None) or not any(tag in tags for tag in route.tags)
    ]

def load_modules_from_path(path: Path):
    reload_env()  # обновляем переменные
    routers = []
    for module_dir in path.iterdir():
        if not module_dir.is_dir():
            continue

        env_var = f"PUBLIC_{module_dir.name.upper()}"
        if os.getenv(env_var, "1") != "1":
            logger.info(f"Модуль public {module_dir.name} отключен в .env ({env_var}=0)")
            continue

        endpoints_file = module_dir / "endpoints.py"
        logic_file = module_dir / "logic.py"

        if not endpoints_file.exists():
            logger.warning(f"Пропущен модуль {module_dir.name}: нет endpoints.py")
            continue

        try:
            # Загружаем logic.py
            logic_module = None
            if logic_file.exists():
                spec = importlib.util.spec_from_file_location(f"{module_dir.name}.logic", logic_file)
                logic_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(logic_module)

            # Загружаем endpoints.py
            spec = importlib.util.spec_from_file_location(f"{module_dir.name}.endpoints", endpoints_file)
            endpoints_module = importlib.util.module_from_spec(spec)
            if logic_module:
                endpoints_module.__dict__["logic"] = logic_module
            spec.loader.exec_module(endpoints_module)

            # Добавляем router
            if hasattr(endpoints_module, "router"):
                old_router: APIRouter = endpoints_module.router
                new_router = APIRouter(
                    prefix=getattr(old_router, "prefix", ""),
                    tags=[module_dir.name]
                )
                for route in old_router.routes:
                    new_router.routes.append(route)
                routers.append(new_router)
            else:
                logger.warning(f"Модуль {module_dir.name} не содержит router")

        except Exception as e:
            logger.error(f"Не удалось загрузить модуль {module_dir.name}: {e}")

    return routers

def load_public_modules():
    return load_modules_from_path(PUBLIC_MODULES_PATH)
