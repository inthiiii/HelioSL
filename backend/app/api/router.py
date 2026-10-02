from fastapi import APIRouter

from app.api.routes import (
    analytics,
    assistant,
    assistant_stream,
    auth,
    energy,
    health,
    integration,
    planning,
    knowledge,
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

api_router.include_router(
    integration.router,
    prefix="/integration",
    tags=["Integrated Intelligence"],
)

api_router.include_router(
    assistant.router,
    prefix="/assistant",
    tags=["AI Assistant"],
)

api_router.include_router(
    assistant_stream.router,
    prefix="/assistant",
    tags=["AI Assistant"],
)

api_router.include_router(
    knowledge.router,
    prefix="/knowledge",
    tags=["Knowledge Retrieval"],
)

api_router.include_router(
    planning.router,
    prefix="/planning",
    tags=["Solar & Financial Planning"],
)
