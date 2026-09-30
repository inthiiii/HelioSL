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

    average_consumption = energy.get(
        "average_consumption_kwh"
    )

    latest_consumption = energy.get(
        "latest_consumption_kwh"
    )

    average_generation = energy.get(
        "average_generation_kwh"
    )

    requested_capacity = entities.get(
        "capacity_kw"
    )

    estimated_daily_consumption = None

    if average_consumption is not None:
        estimated_daily_consumption = round(
            average_consumption / 30,
            2,
        )

    result = {
        "average_monthly_consumption_kwh":
            average_consumption,

        "estimated_daily_consumption_kwh":
            estimated_daily_consumption,

        "latest_consumption_kwh":
            latest_consumption,

        "average_generation_kwh":
            average_generation,

        "requested_capacity_kw":
            requested_capacity,

        "financial_calculation_ready":
            False,

        "financial_note": (
            "Verified tariff data, installation "
            "cost and applicable solar scheme "
            "information are required before "
            "calculating an estimated payback "
            "period."
        ),
    }

    trace = list(
        state.get("trace", [])
    )

    trace.append(
        "Financial and Solar Planning Agent "
        "prepared consumption and solar-planning "
        "context."
    )

    return {
        **state,
        "financial_result": result,
        "trace": trace,
    }

