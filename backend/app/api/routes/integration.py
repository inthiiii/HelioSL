from fastapi import (
    APIRouter,
    Depends,
)
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.schemas.integration import (
    IntegratedSummary,
)
from app.security.dependencies import (
    get_current_user,
)
from app.services.integration_service import (
    build_integrated_summary,
)


router = APIRouter()


@router.get(
    "/summary",
    response_model=IntegratedSummary,
)
def read_integrated_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    return build_integrated_summary(
        db,
        current_user,
    )
