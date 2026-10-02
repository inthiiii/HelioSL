from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.api.router import api_router
from app.core.config import settings
from app.security.headers import (
    SecurityHeadersMiddleware,
)
from app.security.rate_limit import limiter
from app.utils.logger import configure_logging


configure_logging()


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "Agentic AI Renewable Energy Intelligence "
        "Platform for Sri Lanka"
    ),
    debug=settings.debug,
)

app.state.limiter = limiter

app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=list(
        {
            settings.frontend_origin,
            "http://localhost:3000",
            "http://127.0.0.1:3000",
        }
    ),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SecurityHeadersMiddleware
)


app.include_router(
    api_router,
    prefix=settings.api_v1_prefix,
)


@app.get("/")
async def root():
    return {
        "name": "HelioSL",
        "description": (
            "Agentic AI Renewable Energy "
            "Intelligence Platform for Sri Lanka"
        ),
        "version": settings.app_version,
        "environment": settings.app_env,
    }
