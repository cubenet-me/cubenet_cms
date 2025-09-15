# engine/core/middleware.py
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from engine.core.logger import logger
import time

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int = 10, period: int = 1):
        super().__init__(app)
        self.max_requests = max_requests
        self.period = period  # время в секундах
        self.clients = {}     # хранение времени запросов по IP

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        now = time.time()
        request_times = self.clients.get(client_ip, [])
        # Убираем старые запросы
        request_times = [t for t in request_times if now - t < self.period]
        if len(request_times) >= self.max_requests:
            logger.warning(f"IP {client_ip} превысил лимит запросов")
            return JSONResponse(status_code=429, content={"detail": "Too Many Requests"})
        request_times.append(now)
        self.clients[client_ip] = request_times
        response = await call_next(request)
        return response

def setup_middlewares(app):
    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Rate limiting (DDoS protection)
    app.add_middleware(RateLimitMiddleware, max_requests=20, period=1)  # пример: 20 запросов в 1 секунду

    # Logging middleware
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        logger.info(f"Request: {request.method} {request.url}")
        response = await call_next(request)
        logger.info(f"Response status: {response.status_code}")
        return response
