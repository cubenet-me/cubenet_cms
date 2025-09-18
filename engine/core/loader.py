# engine/core/loader.py
import importlib.util
from pathlib import Path
from fastapi import FastAPI
from engine.core.logger.logger import logger

CORE_MODULES_PATH = Path(__file__).parent

def load_core_modules(app: FastAPI):
    for module_dir in CORE_MODULES_PATH.iterdir():
        if not module_dir.is_dir() or module_dir.name in ["__pycache__", "role"]:
            continue

        init_file = module_dir / "__init__.py"
        if not init_file.exists():
            logger.warning(f"Пропущен модуль {module_dir.name}: нет __init__.py")
            continue

        try:
            spec = importlib.util.spec_from_file_location(f"engine.core.{module_dir.name}", init_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            logger.info(f"Модуль core {module_dir.name} загружен")

            if hasattr(module, "setup"):
                module.setup(app)
                logger.info(f"Функция setup вызвана для модуля {module_dir.name}")
            else:
                logger.warning(f"Модуль {module_dir.name} не содержит функцию setup")

        except Exception as e:
            logger.error(f"Не удалось загрузить модуль {module_dir.name}: {e}")