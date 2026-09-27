from fastapi import APIRouter, Depends

from app.llm.client import get_llm_client
from app.models.user import User
from app.security.dependencies import get_current_user


router = APIRouter()


@router.get("/health")
def assistant_health(
    current_user: User = Depends(get_current_user),
):
    client = get_llm_client()

    return {
        "status": (
            "healthy"
            if client.health()
            else "unavailable"
        )
    }