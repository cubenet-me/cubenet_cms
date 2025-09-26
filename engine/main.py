from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from engine.core.logger.logger import logger
from engine.core.loader import load_core_modules
from engine.api.loader import load_public_modules, reload_env, remove_public_routes
from engine.core.config.config import get_settings
from pathlib import Path
import asyncio

# --- Настройки ---
settings = get_settings()

# --- Глобальный лимитер ---
limiter = Limiter(key_func=get_remote_address)

# --- Декоратор для эндпоинтов ---
def slowapi(limit: str):
    def decorator(func):
        return limiter.limit(limit)(func)
    return decorator

# --- Инициализация приложения ---
def init_app(app):
    app.state.limiter = limiter
    app.add_middleware(SlowAPIMiddleware)

    @app.exception_handler(RateLimitExceeded)
    async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
        return JSONResponse(status_code=429, content={"detail": "Too Many Requests"})

app = FastAPI(title="CubeNet CMS")

# Подключаем slowapi
init_app(app)

# Загружаем модули core
load_core_modules(app)

# Подключаем публичные модули
public_routers = load_public_modules()
for router in public_routers:
    app.include_router(router, prefix="/api")

# Список тегов всех публичных модулей
PUBLIC_MODULE_TAGS = [r.tags[0] for r in public_routers]

# Асинхронное наблюдение за .env для публичных модулей
async def watch_public_modules():
    from watchfiles import awatch
    global PUBLIC_MODULE_TAGS

    async for _ in awatch(Path(".env")):
        logger.info("Обнаружено изменение в .env, обновление публичных роутеров...")

        # Перезагружаем переменные окружения
        reload_env()

        # Удаляем старые роутеры по тегам
        remove_public_routes(app, PUBLIC_MODULE_TAGS)

        # Загружаем и подключаем новые роутеры
        new_routers = load_public_modules()
        for router in new_routers:
            app.include_router(router, prefix="/api")

        # Обновляем список тегов
        PUBLIC_MODULE_TAGS = [r.tags[0] for r in new_routers]

        logger.info("Публичные роутеры обновлены")

# Запускаем watcher в фоне
asyncio.create_task(watch_public_modules())

# --- Корневой эндпоинт ---
if settings.root_endpoint:
    @app.get("/", include_in_schema=False)
    @slowapi("3/minute")
    async def root(request: Request):
        return JSONResponse({"message": "CubeNet CMS API running. Static site served via Nginx."})
else:
    @app.get("/", include_in_schema=False)
    async def root_404(request: Request):
        return JSONResponse(status_code=404, content={"detail": "Not Found"})

# --- Обработчики ошибок ---
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(status_code=404, content={"detail": "Not Found"})

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    logger.error(f"Internal server error: {exc}")
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})
