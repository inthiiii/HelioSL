from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.auth import RegisterRequest
from app.security.password import (
    hash_password,
    verify_password,
)
from app.services.user_service import get_user_by_email


def register_user(
    db: Session,
    data: RegisterRequest,
) -> User:

    user = User(
        full_name=data.full_name,
        email=data.email,
        hashed_password=hash_password(
            data.password
        ),
        district=data.district,
        user_type=data.user_type,
        role="user",
        is_active=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def authenticate_user(
    db: Session,
    email: str,
    password: str,
) -> User | None:

    user = get_user_by_email(
        db,
        email,
    )

    if not user:
        return None

    if not verify_password(
        password,
        user.hashed_password,
    ):
        return None

    if not user.is_active:
        return None

    return user