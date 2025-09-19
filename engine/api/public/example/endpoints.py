from fastapi import APIRouter, FastAPI
from engine.core.loader import core_modules

router = APIRouter(prefix="/example", tags=["example"])

# создаём тестовый app для функций setup
test_app = FastAPI()

@router.get("/endpoint")
def example_endpoint():
    result_data = {}

    # --- security ---
    if "security" in core_modules:
        sec = core_modules["security"]
        if "permission_required" in sec:
            try:
                result_data["permission_required"] = sec["permission_required"](level=1)
            except Exception as e:
                result_data["permission_required"] = f"Ошибка: {e}"
        if "setup" in sec:
            try:
                result_data["security_setup"] = sec["setup"](test_app)
            except Exception as e:
                result_data["security_setup"] = f"Ошибка: {e}"

    # --- config ---
    if "config" in core_modules:
        cfg = core_modules["config"]
        if "generate_random_string" in cfg:
            try:
                result_data["generate_random_string"] = cfg["generate_random_string"]()
            except Exception as e:
                result_data["generate_random_string"] = f"Ошибка: {e}"
        if "setup" in cfg:
            try:
                result_data["config_setup"] = cfg["setup"](test_app)
            except Exception as e:
                result_data["config_setup"] = f"Ошибка: {e}"

    # --- logger ---
    if "logger" in core_modules:
        log = core_modules["logger"]
        for fn_name in ["NotFoundException", "UnauthorizedException", "setup"]:
            if fn_name in log:
                try:
                    # setup у logger тоже требует app
                    if fn_name == "setup":
                        result_data[fn_name] = log[fn_name](test_app)
                    else:
                        result_data[fn_name] = str(log[fn_name]())
                except Exception as e:
                    result_data[fn_name] = f"Ошибка: {e}"

    # --- events ---
    if "events" in core_modules:
        ev = core_modules["events"]
        for fn_name in ["setup", "setup_events"]:
            if fn_name in ev:
                try:
                    result_data[fn_name] = ev[fn_name](test_app)
                except Exception as e:
                    result_data[fn_name] = f"Ошибка: {e}"

    return {"message": "Результаты вызова core функций", "result": result_data}
