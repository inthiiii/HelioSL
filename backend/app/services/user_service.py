from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate


def create_user(
    db: Session,
    data: UserCreate,
) -> User:

    user = User(**data.model_dump())

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def get_user(
    db: Session,
    user_id: int,
) -> User | None:

    return db.get(User, user_id)


def get_user_by_email(
    db: Session,
    email: str,
) -> User | None:

    statement = select(User).where(
        User.email == email
    )

    return db.scalar(statement)