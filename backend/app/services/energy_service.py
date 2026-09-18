from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.energy import (
    ConsumptionRecord,
    EnergyProfile,
)
from app.schemas.energy import (
    ConsumptionCreate,
    EnergyProfileCreate,
)


def create_energy_profile(
    db: Session,
    user_id: int,
    data: EnergyProfileCreate,
) -> EnergyProfile:

    profile = EnergyProfile(
        user_id=user_id,
        **data.model_dump(),
    )

    db.add(profile)
    db.commit()
    db.refresh(profile)

    return profile


def get_energy_profile(
    db: Session,
    user_id: int,
) -> EnergyProfile | None:

    statement = select(
        EnergyProfile
    ).where(
        EnergyProfile.user_id == user_id
    )

    return db.scalar(statement)


def create_consumption_record(
    db: Session,
    user_id: int,
    data: ConsumptionCreate,
) -> ConsumptionRecord:

    record = ConsumptionRecord(
        user_id=user_id,
        **data.model_dump(),
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record


def get_consumption_records(
    db: Session,
    user_id: int,
) -> list[ConsumptionRecord]:

    statement = (
        select(ConsumptionRecord)
        .where(
            ConsumptionRecord.user_id
            == user_id
        )
        .order_by(
            ConsumptionRecord.billing_month
        )
    )

    return list(
        db.scalars(statement).all()
    )