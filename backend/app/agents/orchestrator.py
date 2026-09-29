from app.agents.state import AgentState


def orchestrator_agent(
    state: AgentState,
) -> AgentState:

    intent = state.get(
        "intent",
        "general",
    )

    selected_agents: list[str] = []

    if intent == "energy_usage":
        selected_agents.append(
            "energy"
        )

    elif intent == "solar_performance":
        selected_agents.extend(
            [
                "energy",
                "knowledge",
            ]
        )

    elif intent == "solar_scheme":
        selected_agents.extend(
            [
                "knowledge",
                "financial",
            ]
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