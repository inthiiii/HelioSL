from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.user import (
    UserCreate,
    UserResponse,
)
from app.services.user_service import (
    create_user,
    get_user,
    get_user_by_email,
)


router = APIRouter()


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_user(
    data: UserCreate,
    db: Session = Depends(get_db),
):
    existing = get_user_by_email(
        db,
        data.email,
    )

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Email already registered",
        )

    return create_user(db, data)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
)
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    user = get_user(db, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return user