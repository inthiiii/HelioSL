import pytest

from app.services.confidence_service import (
    determine_confidence,
)


@pytest.mark.parametrize(
    ("state", "expected"),
    [
        (
            {
                "sources": [{"title": "PUCSL guideline"}],
                "energy_result": {
                    "latest_generation_kwh": 500.0,
                },
                "safety_notes": [],
            },
            "high",
        ),
        (
            {
                "sources": [{"title": "PUCSL guideline"}],
                "energy_result": {},
                "safety_notes": [],
            },
            "medium",
        ),
        (
            {
                "sources": [],
                "energy_result": {},
                "safety_notes": ["Evidence is incomplete."],
            },
            "low",
        ),
    ],
)
def test_determine_confidence_uses_conservative_levels(
    state,
    expected,
):
    assert determine_confidence(state) == expected
