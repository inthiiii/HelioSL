from app.agents.orchestrator import orchestrator_agent


def selected_agents(
    intent: str,
    query: str,
) -> list[str]:
    result = orchestrator_agent(
        {
            "intent": intent,
            "normalized_query": query,
            "trace": [],
        }
    )

    return result["selected_agents"]


def test_solar_performance_selects_weather():
    assert selected_agents(
        "solar_performance",
        "Why has my solar generation dropped?",
    ) == [
        "energy",
        "knowledge",
        "weather",
    ]


def test_solar_planning_selects_weather():
    assert selected_agents(
        "solar_planning",
        "Should I install a 5 kW solar system?",
    ) == [
        "energy",
        "knowledge",
        "financial",
        "weather",
    ]


def test_ordinary_energy_usage_does_not_select_weather():
    assert selected_agents(
        "energy_usage",
        "Why is my electricity usage increasing?",
    ) == ["energy"]


def test_energy_usage_with_weather_selects_weather():
    assert selected_agents(
        "energy_usage",
        "Does cloudy weather affect my electricity usage?",
    ) == ["energy", "weather"]


def test_scheme_explanation_uses_knowledge_only():
    assert selected_agents(
        "solar_scheme",
        "Explain Net Metering in Sri Lanka.",
    ) == ["knowledge"]


def test_scheme_recommendation_also_uses_financial():
    assert selected_agents(
        "solar_scheme",
        "Which solar scheme is suitable for me?",
    ) == ["knowledge", "financial"]
