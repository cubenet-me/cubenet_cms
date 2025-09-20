from fastapi import FastAPI
from fastapi.responses import JSONResponse
from engine.core.logger.logger import logger
from engine.core.loader import load_core_modules
from engine.api.loader import load_public_modules, reload_env, remove_public_routes
from pathlib import Path
import asyncio

app = FastAPI(title="CubeNet CMS")

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
    global PUBLIC_MODULE_TAGS  # обязательно в начале функции

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

# Корневой эндпоинт
@app.get("/", include_in_schema=False)
async def root():
    return JSONResponse({"message": "CubeNet CMS API running. Static site served via Nginx."})

# Обработчики ошибок
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(status_code=404, content={"detail": "Not Found"})

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    logger.error(f"Internal server error: {exc}")
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})
