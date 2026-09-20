from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.models.user import User
from app.security.dependencies import get_current_user

from app.core.database import get_db
from app.schemas.energy import (
    ConsumptionCreate,
    ConsumptionResponse,
    EnergyProfileCreate,
    EnergyProfileResponse,
)
from app.services.energy_service import (
    create_consumption_record,
    create_energy_profile,
    get_consumption_records,
    get_energy_profile,
)
from app.services.user_service import get_user


router = APIRouter()


@router.post(
    "/me/profile",
    response_model=EnergyProfileResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_energy_profile(
    data: EnergyProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    if get_energy_profile(
        db,
        current_user.id,
    ):
        raise HTTPException(
            status_code=409,
            detail="Energy profile already exists",
        )

    return create_energy_profile(
        db,
        current_user.id,
        data,
    )


@router.get(
    "/me/profile",
    response_model=EnergyProfileResponse,
)
def read_energy_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    profile = get_energy_profile(
        db,
        current_user.id,
    )

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Energy profile not found",
        )

    return profile


@router.post(
    "/me/consumption",
    response_model=ConsumptionResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_consumption(
    data: ConsumptionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    try:
        return create_consumption_record(
            db,
            current_user.id,
            data,
        )

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail=(
                "Consumption record already exists "
                "for this month"
            ),
        )

@router.get(
    "/me/consumption",
    response_model=list[ConsumptionResponse],
)
def read_consumption(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    return get_consumption_records(
        db,
        current_user.id,
    )