from app.agents.state import AgentState


def run_financial_agent(
    state: AgentState,
) -> AgentState:

    energy = state.get(
        "energy_result",
        {},
    )

    entities = state.get(
        "entities",
        {},
    )

    knowledge = state.get(
        "knowledge_result",
        {},
    )

    weather = state.get(
        "weather_result",
        {},
    )

    average_consumption = (
        energy.get(
            "average_consumption_kwh"
        )
    )

    requested_capacity = (
        entities.get(
            "capacity_kw"
        )
    )

    requested_energy = (
        entities.get(
            "energy_kwh"
        )
    )

    missing_inputs: list[str] = []

    if average_consumption is None:
        if requested_energy is not None:
            average_consumption = (
                requested_energy
            )
        else:
            missing_inputs.append(
                "monthly_consumption"
            )

    if requested_capacity is None:
        missing_inputs.append(
            "system_capacity_kw"
        )

    trusted_knowledge_available = (
        knowledge.get(
            "result_count",
            0,
        )
        > 0
    )

    result = {
        "monthly_consumption_kwh":
            average_consumption,

        "requested_capacity_kw":
            requested_capacity,

        "trusted_knowledge_available":
            trusted_knowledge_available,

        "weather_available":
            weather.get(
                "available",
                False,
            ),

        "financial_calculation_ready":
            False,

        "missing_inputs":
            missing_inputs,

        "note": (
            "Full savings and payback estimates "
            "require verified tariff, export-rate, "
            "installation-cost and solar-yield "
            "inputs."
        ),
    }

    trace = list(
        state.get(
            "trace",
            [],
        )
    )

    trace.append(
        "Financial & Solar Planning Agent "
        "evaluated available planning inputs."
    )

    return {
        **state,
        "financial_result":
            result,

        "trace":
            trace,
    }