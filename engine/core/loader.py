# engine/core/loader.py
import importlib.util
from pathlib import Path
from fastapi import FastAPI
from engine.core.logger.logger import logger
import os
from dotenv import load_dotenv

load_dotenv()

CORE_MODULES_PATH = Path(__file__).parent
core_modules = {}  # Словарь для хранения функций всех модулей core

def load_core_modules(app: FastAPI):
    global core_modules
    for module_dir in CORE_MODULES_PATH.iterdir():
        if not module_dir.is_dir() or module_dir.name in ["__pycache__", "role"]:
            continue

        # Проверка .env: CORE_<module_name_upper>=1
        env_var = f"CORE_{module_dir.name.upper()}"
        if os.getenv(env_var, "1") != "1":
            logger.info(f"Модуль core {module_dir.name} отключен в .env ({env_var}=0)")
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

            # Собираем все публичные функции модуля
            core_modules[module_dir.name] = {
                name: getattr(module, name)
                for name in dir(module)
                if callable(getattr(module, name)) and not name.startswith("_")
            }
            logger.info(f"Загружены функции модуля {module_dir.name}: {list(core_modules[module_dir.name].keys())}")

            if hasattr(module, "setup"):
                module.setup(app)
                logger.info(f"Функция setup вызвана для модуля {module_dir.name}")
            else:
                logger.warning(f"Модуль {module_dir.name} не содержит функцию setup")

        except Exception as e:
            logger.error(f"Не удалось загрузить модуль {module_dir.name}: {e}")