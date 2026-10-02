from app.services.assistant_context_service import (
    add_user_context,
)


def test_saved_district_fills_missing_location():
    result = add_user_context(
        {
            "location": None,
            "capacity_kw": 5.0,
        },
        "Colombo",
    )

    assert result["location"] == "Colombo"
    assert result["capacity_kw"] == 5.0


def test_explicit_location_is_preserved():
    result = add_user_context(
        {"location": "Kandy"},
        "Colombo",
    )

    assert result["location"] == "Kandy"
