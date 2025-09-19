# engine/core/events/events.py
from fastapi import FastAPI
from engine.core.logger.logger import logger
import os
from dotenv import load_dotenv

load_dotenv()

ENABLE_SWAGGER = os.getenv("ENABLE_SWAGGER", "1") == "1"
ENABLE_REDOC = os.getenv("ENABLE_REDOC", "1") == "1"
ENABLE_OPENAPI = os.getenv("ENABLE_OPENAPI", "1") == "1"

def setup(app: FastAPI):
    @app.on_event("startup")
    async def on_startup():
        logger.info("CubeNet CMS is starting...")
        logger.info(f"Swagger Docs Enabled: {ENABLE_SWAGGER}")
        logger.info(f"Redoc Docs Enabled: {ENABLE_REDOC}")
        logger.info(f"OpenAPI Enabled: {ENABLE_OPENAPI}")

    @app.on_event("shutdown")
    async def on_shutdown():
        logger.info("CubeNet CMS is shutting down...")