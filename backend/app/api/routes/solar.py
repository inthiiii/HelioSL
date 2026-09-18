from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.solar import (
    SolarGenerationCreate,
    SolarGenerationResponse,
    SolarSystemCreate,
    SolarSystemResponse,
)
from app.services.solar_service import (
    create_generation_record,
    create_solar_system,
    get_generation_records,
    get_solar_system,
)
from app.services.user_service import get_user


router = APIRouter()


@router.post(
    "/users/{user_id}/system",
    response_model=SolarSystemResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_solar_system(
    user_id: int,
    data: SolarSystemCreate,
    db: Session = Depends(get_db),
):
    if not get_user(db, user_id):
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    if get_solar_system(db, user_id):
        raise HTTPException(
            status_code=409,
            detail="Solar system already exists",
        )

    return create_solar_system(
        db,
        user_id,
        data,
    )


@router.get(
    "/users/{user_id}/system",
    response_model=SolarSystemResponse,
)
def read_solar_system(
    user_id: int,
    db: Session = Depends(get_db),
):
    system = get_solar_system(
        db,
        user_id,
    )

    if not system:
        raise HTTPException(
            status_code=404,
            detail="Solar system not found",
        )

    return system


@router.post(
    "/systems/{solar_system_id}/generation",
    response_model=SolarGenerationResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_generation(
    solar_system_id: int,
    data: SolarGenerationCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_generation_record(
            db,
            solar_system_id,
            data,
        )

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail=(
                "Generation record already exists "
                "for this month"
            ),
        )


@router.get(
    "/systems/{solar_system_id}/generation",
    response_model=list[
        SolarGenerationResponse
    ],
)
def read_generation(
    solar_system_id: int,
    db: Session = Depends(get_db),
):
    return get_generation_records(
        db,
        solar_system_id,
    )