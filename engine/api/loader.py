# engine/api/loader.py
import importlib.util
from pathlib import Path
from fastapi import APIRouter
from engine.core.logger import logger  # <--- используем единый logger

PUBLIC_MODULES_PATH = Path(__file__).parent / "public"

def load_modules_from_path(path: Path):
    routers = []
    for module_dir in path.iterdir():
        if not module_dir.is_dir():
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
                logger.info(f"Модуль logic {module_dir.name} загружен")

            # Загружаем endpoints.py
            spec = importlib.util.spec_from_file_location(f"{module_dir.name}.endpoints", endpoints_file)
            endpoints_module = importlib.util.module_from_spec(spec)

            if logic_module:
                endpoints_module.__dict__["logic"] = logic_module

            spec.loader.exec_module(endpoints_module)
            logger.info(f"Модуль endpoints {module_dir.name} загружен")

            # Подключаем роутер и автоматически создаём тег
            if hasattr(endpoints_module, "router"):
                old_router: APIRouter = endpoints_module.router

                new_router = APIRouter(
                    prefix=getattr(old_router, "prefix", ""),
                    tags=[module_dir.name]
                )
                # Копируем маршруты
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
