from fastapi import FastAPI
from fastapi.responses import JSONResponse
from engine.core.logger import logger
from engine.core.middleware import setup_middlewares
from engine.core.events import setup_events
from engine.api.loader import load_public_modules

app = FastAPI(title="CubeNet CMS")

# Middleware и события
setup_middlewares(app)
setup_events(app)

# Подключаем публичные модули
public_routers = load_public_modules()
for router in public_routers:
    app.include_router(router, prefix="/api")

# Корневой эндпоинт
@app.get("/", include_in_schema=False)
async def root():
    return JSONResponse({"message": "CubeNet CMS API running. Static site served via Nginx."})

# Ошибки
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(status_code=404, content={"detail": "Not Found"})

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    logger.error(f"Internal server error: {exc}")
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})
