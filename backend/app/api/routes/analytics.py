from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.schemas.analytics import (
    EnergyIntelligenceSummary,
)
from app.security.dependencies import (
    get_current_user,
)
from app.services.analytics_service import (
    analyze_energy_data,
)
from app.services.energy_service import (
    get_consumption_records,
)
from app.services.solar_service import (
    get_generation_records,
    get_solar_system,
)


router = APIRouter()


@router.get(
    "/summary",
    response_model=EnergyIntelligenceSummary,
)
def get_energy_intelligence_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    consumption = get_consumption_records(
        db,
        current_user.id,
    )

    solar_system = get_solar_system(
        db,
        current_user.id,
    )

    generation = []

    if solar_system:
        generation = get_generation_records(
            db,
            solar_system.id,
        )

    return analyze_energy_data(
        consumption,
        generation,
    )