"""Create the synthetic Space Industries business demonstration account."""

from datetime import date
from decimal import Decimal

from sqlalchemy import select

from app.core.database import SessionLocal
from app.models.energy import (
    ConsumptionRecord,
    EnergyProfile,
)
from app.models.solar import (
    SolarGenerationRecord,
    SolarSystem,
)
from app.models.user import User
from app.security.password import hash_password


SPACE_INDUSTRIES_EMAIL = "spaceindustries@gmail.com"
SPACE_INDUSTRIES_PASSWORD = "SpaceIndustries123"


SPACE_INDUSTRIES_CONSUMPTION = [
    ("2025-04-01", 7800, 429000),
    ("2025-05-01", 7950, 437250),
    ("2025-06-01", 8100, 445500),
    ("2025-07-01", 8300, 456500),
    ("2025-08-01", 8450, 464750),
    ("2025-09-01", 8700, 478500),
    ("2025-10-01", 8900, 489500),
    ("2025-11-01", 9150, 503250),
    ("2025-12-01", 9400, 517000),
    ("2026-01-01", 9650, 530750),
    ("2026-02-01", 9900, 544500),
    ("2026-03-01", 10150, 558250),
    ("2026-04-01", 10400, 572000),
    ("2026-05-01", 10700, 588500),
    ("2026-06-01", 10950, 602250),
    ("2026-07-01", 11200, 616000),
    ("2026-08-01", 11500, 632500),
    ("2026-09-01", 11850, 651750),
]


SPACE_INDUSTRIES_GENERATION = [
    ("2025-04-01", 8750, 1520, 570),
    ("2025-05-01", 8420, 1380, 910),
    ("2025-06-01", 7980, 1190, 1310),
    ("2025-07-01", 7720, 1050, 1630),
    ("2025-08-01", 8150, 1160, 1460),
    ("2025-09-01", 8610, 1340, 1430),
    ("2025-10-01", 9130, 1580, 1350),
    ("2025-11-01", 9480, 1720, 1390),
    ("2025-12-01", 9720, 1840, 1520),
    ("2026-01-01", 9860, 1900, 1690),
    ("2026-02-01", 9210, 1640, 2330),
    ("2026-03-01", 9570, 1710, 2290),
    ("2026-04-01", 9020, 1480, 2860),
    ("2026-05-01", 8540, 1260, 3420),
    ("2026-06-01", 8090, 1040, 3900),
    ("2026-07-01", 7840, 910, 4270),
    ("2026-08-01", 8260, 1080, 4320),
    ("2026-09-01", 8730, 1240, 4360),
]


def parse_month(value: str) -> date:
    return date.fromisoformat(value)


def remove_existing_account(db) -> None:
    user = db.scalar(
        select(User).where(
            User.email == SPACE_INDUSTRIES_EMAIL
        )
    )

    if user:
        db.delete(user)
        db.commit()


def create_space_industries(db) -> User:
    user = User(
        full_name="Space Industries",
        email=SPACE_INDUSTRIES_EMAIL,
        hashed_password=hash_password(
            SPACE_INDUSTRIES_PASSWORD
        ),
        district="Gampaha",
        user_type="business",
        role="user",
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    db.add(
        EnergyProfile(
            user_id=user.id,
            provider="CEB",
            connection_type="industrial",
            average_monthly_consumption_kwh=Decimal(
                "9613.89"
            ),
            average_monthly_bill_lkr=Decimal(
                "528763.89"
            ),
        )
    )

    for month, consumption, bill in SPACE_INDUSTRIES_CONSUMPTION:
        db.add(
            ConsumptionRecord(
                user_id=user.id,
                billing_month=parse_month(month),
                consumption_kwh=Decimal(str(consumption)),
                bill_amount_lkr=Decimal(str(bill)),
            )
        )

    solar = SolarSystem(
        user_id=user.id,
        capacity_kw=Decimal("75.00"),
        installation_date=date(2025, 3, 12),
        scheme="SYNTHETIC_NET_ACCOUNTING",
        panel_brand="Synthetic Industrial PV",
        inverter_brand="Synthetic Three-Phase Inverter",
        installer_name="HelioSL Synthetic Commercial Installer",
    )
    db.add(solar)
    db.commit()
    db.refresh(solar)

    for month, generation, exported, imported in SPACE_INDUSTRIES_GENERATION:
        db.add(
            SolarGenerationRecord(
                solar_system_id=solar.id,
                generation_month=parse_month(month),
                generation_kwh=Decimal(str(generation)),
                exported_kwh=Decimal(str(exported)),
                imported_kwh=Decimal(str(imported)),
            )
        )

    db.commit()
    return user


def main() -> None:
    db = SessionLocal()

    try:
        remove_existing_account(db)
        user = create_space_industries(db)

        print("Synthetic Space Industries account created.")
        print(f"User ID: {user.id}")
        print(f"Email: {SPACE_INDUSTRIES_EMAIL}")
        print(f"Password: {SPACE_INDUSTRIES_PASSWORD}")
        print(f"Consumption records: {len(SPACE_INDUSTRIES_CONSUMPTION)}")
        print(f"Solar generation records: {len(SPACE_INDUSTRIES_GENERATION)}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
