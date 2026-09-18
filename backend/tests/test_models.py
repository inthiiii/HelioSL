from datetime import date
from decimal import Decimal

import pytest
from pydantic import ValidationError

from app.schemas.energy import ConsumptionCreate
from app.schemas.solar import SolarSystemCreate
from app.schemas.user import UserCreate


def test_valid_user_schema():
    user = UserCreate(
        full_name="Test User",
        email="test@example.com",
        district="Colombo",
    )

    assert user.email == "test@example.com"


def test_invalid_user_email():
    with pytest.raises(ValidationError):
        UserCreate(
            full_name="Test User",
            email="invalid-email",
        )


def test_negative_solar_capacity_rejected():
    with pytest.raises(ValidationError):
        SolarSystemCreate(
            capacity_kw=Decimal("-5"),
        )


def test_valid_consumption():
    record = ConsumptionCreate(
        billing_month=date(2026, 9, 1),
        consumption_kwh=Decimal("420.50"),
        bill_amount_lkr=Decimal("15000"),
    )

    assert record.consumption_kwh == Decimal(
        "420.50"
    )