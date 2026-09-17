from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings
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


app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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