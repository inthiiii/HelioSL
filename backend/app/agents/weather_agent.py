from app.agents.state import AgentState
from app.services.weather_service import (
    get_weather_context,
)


def run_weather_agent(
    state: AgentState,
) -> AgentState:

    entities = state.get(
        "entities",
        {},
    )

    location = entities.get(
        "location"
    )

    if not location:
        trace = list(
            state.get(
                "trace",
                [],
            )
        )

        trace.append(
            "Weather Agent skipped because "
            "no location was available."
        )

        return {
            **state,
            "weather_result": {
                "available": False,
                "reason":
                    "No location available",
            },
            "trace": trace,
        }

    result = get_weather_context(
        location
    )

    trace = list(
        state.get(
            "trace",
            [],
        )
    )

    if result.get("available"):
        trace.append(
            "Weather Agent retrieved "
            "environmental conditions."
        )
    else:
        trace.append(
            "Weather Agent could not "
            "retrieve weather information."
        )

    return {
        **state,
        "weather_result": result,
        "trace": trace,
    }