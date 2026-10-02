from datetime import date
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import Mock

from fastapi.testclient import TestClient

from app.core.database import get_db
from app.main import app
from app.security.dependencies import (
    get_current_user,
)
from app.services import integration_service


client = TestClient(app)


def test_integrated_summary_returns_household_demo_state(
    monkeypatch,
):
    user = SimpleNamespace(
        id=21,
        user_type="household",
        district="Colombo",
    )
    profile = SimpleNamespace(
        provider="CEB",
        connection_type="domestic",
        average_monthly_consumption_kwh=(
            Decimal("453.67")
        ),
    )
    solar = SimpleNamespace(
        id=31,
        capacity_kw=Decimal("5.00"),
        scheme="DEMO_SCHEME",
        installation_date=date(2025, 1, 15),
    )
    consumption = [
        SimpleNamespace(
            consumption_kwh=Decimal(str(value))
        )
        for value in (
            410,
            425,
            438,
            446,
            455,
            462,
            470,
            482,
            495,
        )
    ]
    generation = [
        SimpleNamespace(
            generation_kwh=Decimal(str(value))
        )
        for value in (
            635,
            620,
            645,
            610,
            590,
            570,
            555,
            525,
            475,
        )
    ]

    monkeypatch.setattr(
        integration_service,
        "get_energy_profile",
        lambda db, user_id: profile,
    )
    monkeypatch.setattr(
        integration_service,
        "get_consumption_records",
        lambda db, user_id: consumption,
    )
    monkeypatch.setattr(
        integration_service,
        "get_solar_system",
        lambda db, user_id: solar,
    )
    monkeypatch.setattr(
        integration_service,
        "get_generation_records",
        lambda db, solar_system_id: generation,
    )
    monkeypatch.setattr(
        integration_service,
        "get_weather_context",
        lambda location: {
            "available": True,
            "location": location,
            "temperature_c": 29.5,
            "humidity_percent": 78,
            "cloud_cover_percent": 80,
            "precipitation_mm": 0.2,
        },
    )

    app.dependency_overrides[get_db] = lambda: Mock()
    app.dependency_overrides[get_current_user] = lambda: user

    try:
        response = client.get(
            "/api/v1/integration/summary"
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200

    data = response.json()

    assert data["user_type"] == "household"
    assert data["district"] == "Colombo"
    assert data["energy_profile_available"] is True
    assert data["solar_system_available"] is True
    assert data["energy"]["average_consumption_kwh"] == 453.67
    assert data["energy"]["latest_consumption_kwh"] == 495
    assert data["energy"]["consumption_change_percent"] == 2.7
    assert data["energy"]["consumption_trend"] == "increasing"
    assert data["energy"]["latest_generation_kwh"] == 475
    assert data["energy"]["generation_change_percent"] == -9.52
    assert data["energy"]["generation_trend"] == "decreasing"
    assert data["solar"]["capacity_kw"] == 5
    assert data["solar"]["record_count"] == 9
    assert data["weather"]["available"] is True
    assert data["weather"]["location"] == "Colombo"
    assert data["alerts"] == [
        "Electricity consumption is increasing.",
        "Solar generation is decreasing.",
    ]
    assert len(data["tips"]) == 3


def test_integrated_summary_requires_authentication():
    response = client.get(
        "/api/v1/integration/summary"
    )

    assert response.status_code in {401, 403}
