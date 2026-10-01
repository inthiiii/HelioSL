from app.agents.state import AgentState


def orchestrator_agent(
    state: AgentState,
) -> AgentState:

    intent = state.get(
        "intent",
        "general",
    )

    selected_agents: list[str] = []

    query = (
        state.get("normalized_query")
        or state.get("original_query", "")
    ).lower()

    weather_mentioned = any(
        term in query
        for term in (
            "weather",
            "cloud",
            "rain",
            "temperature",
            "humidity",
            "sunlight",
            "sunshine",
            "irradiance",
        )
    )

    scheme_decision_requested = any(
        term in query
        for term in (
            "which scheme",
            "suitable",
            "recommend",
            "choose",
            "best scheme",
            "for me",
        )
    )

    if intent == "energy_usage":
        selected_agents.append(
            "energy"
        )

        if weather_mentioned:
            selected_agents.append(
                "weather"
            )

    elif intent == "solar_performance":
        selected_agents.extend(
            [
                "energy",
                "knowledge",
                "weather",
            ]
        )

    elif intent == "solar_scheme":
        selected_agents.append(
            "knowledge"
        )

        if scheme_decision_requested:
            selected_agents.append(
                "financial"
            )

    elif intent == "financial":
        selected_agents.extend(
            [
                "energy",
                "financial",
                "knowledge",
            ]
        )

    elif intent == "solar_planning":
        selected_agents.extend(
            [
                "energy",
                "knowledge",
                "financial",
                "weather",
            ]
        )

    else:
        selected_agents.append(
            "knowledge"
        )

    trace = state.get(
        "trace",
        [],
    )

    trace.append(
        "Orchestrator selected: "
        + ", ".join(selected_agents)
    )

    return {
        **state,
        "selected_agents":
            selected_agents,
        "trace":
            trace,
    }
