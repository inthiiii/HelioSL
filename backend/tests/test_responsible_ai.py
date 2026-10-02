from app.agents.safety_agent import (
    safety_agent,
)
from app.services.confidence_service import (
    determine_confidence,
)


def test_dangerous_electrical_advice_blocked():
    state = {
        "draft_answer": (
            "Open the inverter and touch the wires."
        ),
        "selected_agents": [
            "knowledge"
        ],
        "sources": [],
        "trace": [],
    }

    result = safety_agent(
        state
    )

    assert result["safety_passed"] is False
    assert "touch the wires" not in result["final_answer"].lower()


def test_overconfident_financial_claim_is_flagged():
    result = safety_agent(
        {
            "draft_answer": (
                "This system will definitely provide "
                "guaranteed savings."
            ),
            "selected_agents": ["financial"],
            "financial_result": {
                "financial_calculation_ready": False,
            },
            "sources": [],
            "trace": [],
        }
    )

    assert (
        "Potentially overconfident AI claim detected."
        in result["safety_notes"]
    )
    assert (
        "Financial recommendation is incomplete because "
        "verified planning inputs are missing."
        in result["safety_notes"]
    )


def test_missing_evidence_produces_low_confidence():
    state = {
        "sources": [],
        "energy_result": {
            "latest_consumption_kwh": None,
            "latest_generation_kwh": None,
        },
        "safety_notes": [
            "Insufficient evidence for a supported conclusion."
        ],
    }

    assert determine_confidence(state) == "low"
