# engine/api/loader.py
import importlib
from pathlib import Path

PUBLIC_MODULES_PATH = Path(__file__).parent / "public"

def load_modules_from_path(path: Path, base_package: str):
    routers = []
    for module_dir in path.iterdir():
        if module_dir.is_dir() and (module_dir / "endpoints.py").exists():
            module_name = f"{base_package}.{module_dir.name}.endpoints"
            module = importlib.import_module(module_name)
            if hasattr(module, "router"):
                routers.append(module.router)
    return routers

def load_public_modules():
    return load_modules_from_path(PUBLIC_MODULES_PATH, "engine.api.public")
