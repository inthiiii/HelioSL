from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

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
    "/users/{user_id}/profile",
    response_model=EnergyProfileResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_energy_profile(
    user_id: int,
    data: EnergyProfileCreate,
    db: Session = Depends(get_db),
):
    if not get_user(db, user_id):
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    if get_energy_profile(db, user_id):
        raise HTTPException(
            status_code=409,
            detail="Energy profile already exists",
        )

    return create_energy_profile(
        db,
        user_id,
        data,
    )


@router.get(
    "/users/{user_id}/profile",
    response_model=EnergyProfileResponse,
)
def read_energy_profile(
    user_id: int,
    db: Session = Depends(get_db),
):
    profile = get_energy_profile(
        db,
        user_id,
    )

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Energy profile not found",
        )

    return profile


@router.post(
    "/users/{user_id}/consumption",
    response_model=ConsumptionResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_consumption(
    user_id: int,
    data: ConsumptionCreate,
    db: Session = Depends(get_db),
):
    if not get_user(db, user_id):
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    try:
        return create_consumption_record(
            db,
            user_id,
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
    "/users/{user_id}/consumption",
    response_model=list[ConsumptionResponse],
)
def read_consumption(
    user_id: int,
    db: Session = Depends(get_db),
):
    return get_consumption_records(
        db,
        user_id,
    )