from fastapi import APIRouter

from app.api.routes import (
    auth,
    energy,
    health,
    solar,
    users,
)

from app.api.routes import (
    analytics,
    auth,
    energy,
    health,
    solar,
    users,
)


api_router = APIRouter()

api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"],
)


api_router.include_router(
    health.router,
    prefix="/health",
    tags=["Health"],
)

api_router.include_router(
    users.router,
    prefix="/users",
    tags=["Users"],
)

api_router.include_router(
    energy.router,
    prefix="/energy",
    tags=["Energy"],
)

api_router.include_router(
    solar.router,
    prefix="/solar",
    tags=["Solar"],
)

api_router.include_router(
    analytics.router,
    prefix="/analytics",
    tags=["Energy Intelligence"],
)