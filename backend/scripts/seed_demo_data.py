from datetime import date
from decimal import Decimal

from sqlalchemy import delete, select

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


HOUSEHOLD_EMAIL = "household.demo@heliosl.local"
BUSINESS_EMAIL = "business.demo@heliosl.local"


HOUSEHOLD_CONSUMPTION = [
    ("2026-01-01", 410, 14500),
    ("2026-02-01", 425, 15100),
    ("2026-03-01", 438, 15750),
    ("2026-04-01", 446, 16100),
    ("2026-05-01", 455, 16600),
    ("2026-06-01", 462, 17000),
    ("2026-07-01", 470, 17400),
    ("2026-08-01", 482, 18100),
    ("2026-09-01", 495, 18800),
]

HOUSEHOLD_GENERATION = [
    ("2026-01-01", 635, 280, 105),
    ("2026-02-01", 620, 270, 110),
    ("2026-03-01", 645, 295, 100),
    ("2026-04-01", 610, 265, 115),
    ("2026-05-01", 590, 250, 125),
    ("2026-06-01", 570, 235, 135),
    ("2026-07-01", 555, 220, 145),
    ("2026-08-01", 525, 195, 160),
    ("2026-09-01", 475, 160, 185),
]


BUSINESS_CONSUMPTION = [
    ("2026-01-01", 1850, 114000),
    ("2026-02-01", 1920, 119000),
    ("2026-03-01", 1980, 123000),
    ("2026-04-01", 2050, 128000),
    ("2026-05-01", 2110, 132000),
    ("2026-06-01", 2180, 138000),
    ("2026-07-01", 2240, 143000),
    ("2026-08-01", 2310, 149000),
    ("2026-09-01", 2390, 156000),
]

BUSINESS_GENERATION = [
    ("2026-01-01", 2550, 720, 520),
    ("2026-02-01", 2480, 680, 560),
    ("2026-03-01", 2600, 760, 500),
    ("2026-04-01", 2520, 710, 540),
    ("2026-05-01", 2410, 620, 610),
    ("2026-06-01", 2320, 560, 675),
    ("2026-07-01", 2230, 490, 735),
    ("2026-08-01", 2110, 410, 820),
    ("2026-09-01", 1950, 300, 940),
]


def parse_month(value: str) -> date:
    return date.fromisoformat(value)


def get_user_by_email(db, email: str) -> User | None:
    statement = select(User).where(
        User.email == email
    )

    return db.scalar(statement)


def remove_existing_demo_user(db, email: str) -> None:
    user = get_user_by_email(
        db,
        email,
    )

    if not user:
        return

    # ORM cascade should remove related records.
    db.delete(user)
    db.commit()


def create_household_demo(db) -> User:
    user = User(
        full_name="HelioSL Household Demo",
        email=HOUSEHOLD_EMAIL,
        hashed_password=hash_password(
            "DemoHouse123!"
        ),
        district="Colombo",
        user_type="household",
        role="user",
        is_active=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    profile = EnergyProfile(
        user_id=user.id,
        provider="CEB",
        connection_type="domestic",
        average_monthly_consumption_kwh=Decimal(
            "453.67"
        ),
        average_monthly_bill_lkr=Decimal(
            "16616.67"
        ),
    )

    db.add(profile)

    for (
        month,
        consumption,
        bill,
    ) in HOUSEHOLD_CONSUMPTION:
        db.add(
            ConsumptionRecord(
                user_id=user.id,
                billing_month=parse_month(month),
                consumption_kwh=Decimal(
                    str(consumption)
                ),
                bill_amount_lkr=Decimal(
                    str(bill)
                ),
            )
        )

    solar = SolarSystem(
        user_id=user.id,
        capacity_kw=Decimal("5.00"),
        installation_date=date(
            2025,
            1,
            15,
        ),
        scheme="DEMO_SCHEME",
        panel_brand="Demo PV",
        inverter_brand="Demo Inverter",
        installer_name="HelioSL Demo Installer",
    )

    db.add(solar)
    db.commit()
    db.refresh(solar)

    for (
        month,
        generation,
        exported,
        imported,
    ) in HOUSEHOLD_GENERATION:
        db.add(
            SolarGenerationRecord(
                solar_system_id=solar.id,
                generation_month=parse_month(
                    month
                ),
                generation_kwh=Decimal(
                    str(generation)
                ),
                exported_kwh=Decimal(
                    str(exported)
                ),
                imported_kwh=Decimal(
                    str(imported)
                ),
            )
        )

    db.commit()

    return user


def create_business_demo(db) -> User:
    user = User(
        full_name="HelioSL Business Demo",
        email=BUSINESS_EMAIL,
        hashed_password=hash_password(
            "DemoBiz123!"
        ),
        district="Gampaha",
        user_type="business",
        role="user",
        is_active=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    profile = EnergyProfile(
        user_id=user.id,
        provider="CEB",
        connection_type="commercial",
        average_monthly_consumption_kwh=Decimal(
            "2114.44"
        ),
        average_monthly_bill_lkr=Decimal(
            "133555.56"
        ),
    )

    db.add(profile)

    for (
        month,
        consumption,
        bill,
    ) in BUSINESS_CONSUMPTION:
        db.add(
            ConsumptionRecord(
                user_id=user.id,
                billing_month=parse_month(month),
                consumption_kwh=Decimal(
                    str(consumption)
                ),
                bill_amount_lkr=Decimal(
                    str(bill)
                ),
            )
        )

    solar = SolarSystem(
        user_id=user.id,
        capacity_kw=Decimal("20.00"),
        installation_date=date(
            2024,
            8,
            10,
        ),
        scheme="DEMO_SCHEME",
        panel_brand="Demo Commercial PV",
        inverter_brand="Demo Commercial Inverter",
        installer_name="HelioSL Demo Commercial Installer",
    )

    db.add(solar)
    db.commit()
    db.refresh(solar)

    for (
        month,
        generation,
        exported,
        imported,
    ) in BUSINESS_GENERATION:
        db.add(
            SolarGenerationRecord(
                solar_system_id=solar.id,
                generation_month=parse_month(
                    month
                ),
                generation_kwh=Decimal(
                    str(generation)
                ),
                exported_kwh=Decimal(
                    str(exported)
                ),
                imported_kwh=Decimal(
                    str(imported)
                ),
            )
        )

    db.commit()

    return user


def main() -> None:
    db = SessionLocal()

    try:
        print(
            "Removing previous synthetic demo users..."
        )

        remove_existing_demo_user(
            db,
            HOUSEHOLD_EMAIL,
        )

        remove_existing_demo_user(
            db,
            BUSINESS_EMAIL,
        )

        print(
            "Creating household demo..."
        )

        household = create_household_demo(
            db
        )

        print(
            f"Household created with ID "
            f"{household.id}"
        )

        print(
            "Creating business demo..."
        )

        business = create_business_demo(
            db
        )

        print(
            f"Business created with ID "
            f"{business.id}"
        )

        print()
        print(
            "Synthetic HelioSL demo data ready."
        )

        print()
        print(
            "Household login:"
        )

        print(
            HOUSEHOLD_EMAIL
        )

        print(
            "Password: DemoHouse123!"
        )

        print()
        print(
            "Business login:"
        )

        print(
            BUSINESS_EMAIL
        )

        print(
            "Password: DemoBiz123!"
        )

    finally:
        db.close()


if __name__ == "__main__":
    main()