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

from app.models.user import User
from app.security.dependencies import get_current_user


router = APIRouter()


@router.post(
    "/me/system",
    response_model=SolarSystemResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_solar_system(
    data: SolarSystemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    if get_solar_system(
        db,
        current_user.id,
    ):
        raise HTTPException(
            status_code=409,
            detail="Solar system already exists",
        )

    return create_solar_system(
        db,
        current_user.id,
        data,
    )


@router.get(
    "/me/system",
    response_model=SolarSystemResponse,
)
def read_solar_system(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    system = get_solar_system(
        db,
        current_user.id,
    )

    if not system:
        raise HTTPException(
            status_code=404,
            detail="Solar system not found",
        )

    return system


@router.post(
    "/me/generation",
    response_model=SolarGenerationResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_generation(
    data: SolarGenerationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    system = get_solar_system(
        db,
        current_user.id,
    )

    if not system:
        raise HTTPException(
            status_code=404,
            detail="Solar system not found",
        )

    try:
        return create_generation_record(
            db,
            system.id,
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
    "/me/generation",
    response_model=list[
        SolarGenerationResponse
    ],
)
def read_generation(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    system = get_solar_system(
        db,
        current_user.id,
    )

    if not system:
        raise HTTPException(
            status_code=404,
            detail="Solar system not found",
        )

    return get_generation_records(
        db,
        system.id,
    )