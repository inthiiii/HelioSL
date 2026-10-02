from typing import Literal

from app.agents.state import AgentState


def determine_confidence(
    state: AgentState,
) -> Literal["high", "medium", "low"]:

    sources = state.get(
        "sources",
        [],
    )

    energy = state.get(
        "energy_result",
        {},
    )

    score = 0

    if sources:
        score += 1

    if (
        energy.get(
            "latest_consumption_kwh"
        ) is not None
        or energy.get(
            "latest_generation_kwh"
        ) is not None
    ):
        score += 1

    if not state.get(
        "safety_notes"
    ):
        score += 1

    if score >= 3:
        return "high"

    if score == 2:
        return "medium"

    return "low"
