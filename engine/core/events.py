from fastapi import FastAPI
from engine.core.logger import logger
from engine.core.security import ENABLE_SWAGGER, ENABLE_REDOC, ENABLE_OPENAPI

def setup_events(app: FastAPI):
    @app.on_event("startup")
    async def on_startup():
        logger.info("CubeNet CMS is starting...")
        logger.info(f"Swagger Docs Enabled: {ENABLE_SWAGGER}")
        logger.info(f"Redoc Docs Enabled: {ENABLE_REDOC}")
        logger.info(f"OpenAPI Enabled: {ENABLE_OPENAPI}")

    @app.on_event("shutdown")
    async def on_shutdown():
        logger.info("CubeNet CMS is shutting down...")
