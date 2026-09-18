from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.solar import (
    SolarGenerationRecord,
    SolarSystem,
)
from app.schemas.solar import (
    SolarGenerationCreate,
    SolarSystemCreate,
)


def create_solar_system(
    db: Session,
    user_id: int,
    data: SolarSystemCreate,
) -> SolarSystem:

    system = SolarSystem(
        user_id=user_id,
        **data.model_dump(),
    )

    db.add(system)
    db.commit()
    db.refresh(system)

    return system


def get_solar_system(
    db: Session,
    user_id: int,
) -> SolarSystem | None:

    statement = select(
        SolarSystem
    ).where(
        SolarSystem.user_id == user_id
    )

    return db.scalar(statement)


def create_generation_record(
    db: Session,
    solar_system_id: int,
    data: SolarGenerationCreate,
) -> SolarGenerationRecord:

    record = SolarGenerationRecord(
        solar_system_id=solar_system_id,
        **data.model_dump(),
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record


def get_generation_records(
    db: Session,
    solar_system_id: int,
) -> list[SolarGenerationRecord]:

    statement = (
        select(SolarGenerationRecord)
        .where(
            SolarGenerationRecord.solar_system_id
            == solar_system_id
        )
        .order_by(
            SolarGenerationRecord.generation_month
        )
    )

    return list(
        db.scalars(statement).all()
    )