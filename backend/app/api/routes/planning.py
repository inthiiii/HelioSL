from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.schemas.planning import (
    SolarPlanningRequest,
    SolarPlanningScenario,
    SolarScenarioComparisonRequest,
    SolarScenarioComparisonResponse,
)
from app.security.dependencies import (
    get_current_user,
)
from app.services.energy_service import (
    get_energy_profile,
)
from app.services.planning_service import (
    calculate_solar_scenario,
    compare_solar_scenarios,
)


router = APIRouter()


@router.post(
    "/scenario",
    response_model=SolarPlanningScenario,
)
def create_solar_scenario(
    data: SolarPlanningRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    profile = get_energy_profile(
        db,
        current_user.id,
    )

    average_consumption = None

    if (
        profile
        and profile.average_monthly_consumption_kwh
        is not None
    ):
        average_consumption = float(
            profile.average_monthly_consumption_kwh
        )

    return calculate_solar_scenario(
        average_consumption,
        data,
    )


@router.post(
    "/compare",
    response_model=
        SolarScenarioComparisonResponse,
)
def compare_system_sizes(
    data: SolarScenarioComparisonRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    profile = get_energy_profile(
        db,
        current_user.id,
    )

    average_consumption = None

    if (
        profile
        and profile.average_monthly_consumption_kwh
        is not None
    ):
        average_consumption = float(
            profile.average_monthly_consumption_kwh
        )

    scenarios = compare_solar_scenarios(
        average_consumption,
        data,
    )

    return SolarScenarioComparisonResponse(
        scenarios=scenarios
    )