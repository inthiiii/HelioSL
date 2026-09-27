from app.nlp.pipeline import analyze_text


def test_solar_planning_intent():
    result = analyze_text(
        "I want to install a 5 kW solar system in Colombo"
    )

    assert result["intent"] == "solar_planning"

    assert result["entities"]["capacity_kw"] == 5.0

    assert result["entities"]["location"] == "Colombo"


def test_energy_usage_intent():
    result = analyze_text(
        "Why is my electricity consumption high?"
    )

    assert result["intent"] == "energy_usage"


def test_query_normalization():
    result = analyze_text(
        "  my   solar   generation  "
    )

    assert (
        result["normalized_query"]
        == "my solar generation"
    )