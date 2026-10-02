from datetime import date
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import Mock, patch

from app.services.analytics_service import (
    analyze_energy_data,
)
from app.services.integration_service import (
    build_integrated_summary,
)


def test_build_integrated_summary_with_complete_data():
    db = Mock()
    user = SimpleNamespace(
        id=7,
        user_type="household",
        district="Colombo",
    )
    profile = SimpleNamespace(
        provider="CEB",
        connection_type="domestic",
        average_monthly_consumption_kwh=(
            Decimal("452.50")
        ),
    )
    solar = SimpleNamespace(
        id=11,
        capacity_kw=Decimal("5.00"),
        scheme="Net Accounting",
        installation_date=date(2024, 1, 15),
    )
    consumption = [Mock(), Mock()]
    generation = [Mock(), Mock(), Mock()]
    analytics = {
        "consumption_trend": "increasing",
        "generation_trend": "decreasing",
        "generation_anomaly": True,
    }

    with (
        patch(
            "app.services.integration_service."
            "get_energy_profile",
            return_value=profile,
        ),
        patch(
            "app.services.integration_service."
            "get_consumption_records",
            return_value=consumption,
        ),
        patch(
            "app.services.integration_service."
            "get_solar_system",
            return_value=solar,
        ),
        patch(
            "app.services.integration_service."
            "get_generation_records",
            return_value=generation,
        ),
        patch(
            "app.services.integration_service."
            "analyze_energy_data",
            return_value=analytics,
        ),
    ):
        result = build_integrated_summary(
            db,
            user,
        )

    assert result["energy_profile_available"] is True
    assert result["solar_system_available"] is True
    assert result["energy"]["provider"] == "CEB"
    assert (
        result["energy"]
        ["profile_average_consumption_kwh"]
        == 452.5
    )
    assert result["solar"]["capacity_kw"] == 5.0
    assert result["solar"]["record_count"] == 3
    assert result["alerts"] == [
        "Electricity consumption is increasing.",
        "Solar generation is decreasing.",
        (
            "Solar generation may be below "
            "the historical baseline."
        ),
    ]


def test_build_integrated_summary_without_optional_data():
    db = Mock()
    user = SimpleNamespace(
        id=8,
        user_type="household",
        district=None,
    )
    analytics = {
        "consumption_trend": "insufficient_data",
        "generation_trend": "insufficient_data",
        "generation_anomaly": False,
    }

    with (
        patch(
            "app.services.integration_service."
            "get_energy_profile",
            return_value=None,
        ),
        patch(
            "app.services.integration_service."
            "get_consumption_records",
            return_value=[],
        ),
        patch(
            "app.services.integration_service."
            "get_solar_system",
            return_value=None,
        ),
        patch(
            "app.services.integration_service."
            "analyze_energy_data",
            return_value=analytics,
        ),
        patch(
            "app.services.integration_service."
            "get_generation_records",
        ) as get_generation,
    ):
        result = build_integrated_summary(
            db,
            user,
        )

    get_generation.assert_not_called()
    assert result["energy_profile_available"] is False
    assert result["solar_system_available"] is False
    assert result["energy"]["provider"] is None
    assert result["solar"]["capacity_kw"] is None
    assert result["solar"]["record_count"] == 0
    assert result["alerts"] == []


def test_gradual_changes_are_detected_as_overall_trends():
    consumption = [
        SimpleNamespace(
            consumption_kwh=Decimal(str(value))
        )
        for value in (410, 425, 438, 446, 455, 462, 470, 482, 495)
    ]
    generation = [
        SimpleNamespace(
            generation_kwh=Decimal(str(value))
        )
        for value in (635, 620, 645, 610, 590, 570, 555, 525, 475)
    ]

    result = analyze_energy_data(
        consumption,
        generation,
    )

    assert result["consumption_change_percent"] == 2.7
    assert result["generation_change_percent"] == -9.52
    assert result["consumption_trend"] == "increasing"
    assert result["generation_trend"] == "decreasing"
