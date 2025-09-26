from fastapi import FastAPI
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.requests import Request

limiter = Limiter(key_func=get_remote_address)

def setup_limiter(app: FastAPI):
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

def slowapi(rate: str):
    return limiter.limit(rate)

def setup(app: FastAPI):
    setup_limiter(app)