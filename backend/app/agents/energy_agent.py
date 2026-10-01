from sqlalchemy.orm import Session

from app.agents.state import AgentState
from app.services.analytics_service import analyze_energy_data
from app.services.energy_service import get_consumption_records
from app.services.solar_service import (
    get_generation_records,
    get_solar_system,
)


def run_energy_agent(
    state: AgentState,
    db: Session,
) -> AgentState:

    user_id = state["user_id"]

    consumption_records = get_consumption_records(
        db,
        user_id,
    )

    solar_system = get_solar_system(
        db,
        user_id,
    )

    generation_records = []

    if solar_system:
        generation_records = get_generation_records(
            db,
            solar_system.id,
        )

    analysis = analyze_energy_data(
        consumption_records,
        generation_records,
    )

    result = {
        "average_consumption_kwh":
            analysis.get("average_consumption_kwh"),

        "latest_consumption_kwh":
            analysis.get("latest_consumption_kwh"),

        "consumption_change_percent":
            analysis.get("consumption_change_percent"),

        "consumption_trend":
            analysis.get("consumption_trend"),

        "average_generation_kwh":
            analysis.get("average_generation_kwh"),

        "latest_generation_kwh":
            analysis.get("latest_generation_kwh"),

        "generation_change_percent":
            analysis.get("generation_change_percent"),

        "generation_trend":
            analysis.get("generation_trend"),

        "generation_anomaly":
            analysis.get("generation_anomaly"),
    }

    trace = list(
        state.get("trace", [])
    )

    trace.append(
        "Energy Intelligence Agent analysed "
        "the user's electricity consumption "
        "and solar generation history."
    )

    return {
        **state,
        "energy_result": result,
        "trace": trace,
    }