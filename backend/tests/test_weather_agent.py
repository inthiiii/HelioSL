from app.agents import weather_agent


def test_weather_agent_skips_without_location():
    result = weather_agent.run_weather_agent(
        {
            "entities": {},
            "trace": [],
        }
    )

    assert result["weather_result"] == {
        "available": False,
        "reason": "No location available",
    }
    assert "no location" in result["trace"][-1].lower()


def test_weather_agent_returns_environmental_context(monkeypatch):
    monkeypatch.setattr(
        weather_agent,
        "get_weather_context",
        lambda location: {
            "available": True,
            "location": location,
            "cloud_cover_percent": 70,
        },
    )

    result = weather_agent.run_weather_agent(
        {
            "entities": {"location": "Colombo"},
            "trace": [],
        }
    )

    assert result["weather_result"]["location"] == "Colombo"
    assert "retrieved" in result["trace"][-1].lower()
