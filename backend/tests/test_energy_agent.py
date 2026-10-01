from app.services.analytics_service import (
    percentage_change,
    trend_from_change,
)


def test_percentage_change():
    result = percentage_change(
        500,
        400,
    )

    assert result == -20.0


def test_decreasing_trend():
    assert (
        trend_from_change(-10)
        == "decreasing"
    )


def test_stable_trend():
    assert (
        trend_from_change(2)
        == "stable"
    )