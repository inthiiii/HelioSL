from types import SimpleNamespace

from fastapi.testclient import TestClient

from app.api.routes import assistant
from app.agents.safety_agent import safety_agent
from app.core.database import get_db
from app.main import app
from app.security.dependencies import get_current_user


def test_missing_solar_performance_sources_prevent_causal_claims():
    result = safety_agent(
        {
            "intent": "solar_performance",
            "selected_agents": ["energy", "knowledge"],
            "energy_result": {
                "latest_generation_kwh": 480.0,
                "generation_change_percent": -15.79,
            },
            "sources": [],
            "draft_answer": "The drop was caused by shading.",
            "trace": [],
        }
    )

    assert result["safety_passed"] is True
    assert "does not establish its cause" in result["final_answer"]
    assert "No trusted knowledge source" in result["final_answer"]
    assert "caused by shading" not in result["final_answer"]


def test_missing_solar_metrics_do_not_claim_measured_decrease():
    result = safety_agent(
        {
            "intent": "solar_performance",
            "selected_agents": ["energy", "knowledge"],
            "energy_result": {
                "latest_generation_kwh": None,
                "generation_change_percent": None,
            },
            "sources": [],
            "draft_answer": (
                "None kWh and None% confirms a measured decrease."
            ),
            "trace": [],
        }
    )

    answer = result["final_answer"]

    assert "No solar-generation records" in answer
    assert "cannot confirm that generation has dropped" in answer
    assert "None kWh" not in answer
    assert "None%" not in answer
    assert "measured decrease" not in answer


def test_single_solar_record_is_not_reported_as_a_drop():
    result = safety_agent(
        {
            "intent": "solar_performance",
            "selected_agents": ["energy", "knowledge"],
            "energy_result": {
                "latest_generation_kwh": 480.0,
                "generation_change_percent": None,
            },
            "sources": [],
            "draft_answer": "Generation decreased.",
            "trace": [],
        }
    )

    answer = result["final_answer"]

    assert "480 kWh" in answer
    assert "no usable preceding record" in answer
    assert "cannot confirm that generation has dropped" in answer


def test_missing_consumption_metrics_are_explained_clearly():
    result = safety_agent(
        {
            "intent": "energy_usage",
            "selected_agents": ["energy"],
            "energy_result": {
                "latest_consumption_kwh": None,
                "consumption_change_percent": None,
            },
            "sources": [],
            "draft_answer": "Your usage increased by None%.",
            "trace": [],
        }
    )

    answer = result["final_answer"]

    assert "No electricity-consumption records" in answer
    assert "cannot confirm that usage is increasing" in answer
    assert "None" not in answer


def test_dangerous_electrical_instruction_is_replaced():
    result = safety_agent(
        {
            "intent": "solar_performance",
            "selected_agents": ["energy"],
            "draft_answer": (
                "Open the inverter and touch the wires to test it."
            ),
            "trace": [],
        }
    )

    assert result["safety_passed"] is False
    assert "potentially unsafe electrical guidance" in result[
        "final_answer"
    ]
    assert "touch the wires" not in result["final_answer"]
    assert result["safety_notes"] == [
        "Potentially unsafe electrical instruction detected.",
    ]


def test_missing_scheme_sources_prevent_scheme_recommendation():
    result = safety_agent(
        {
            "intent": "solar_scheme",
            "selected_agents": ["knowledge", "financial"],
            "knowledge_result": {
                "result_count": 0,
                "context": "",
            },
            "financial_result": {
                "financial_calculation_ready": False,
            },
            "sources": [],
            "draft_answer": "Choose Net Accounting.",
            "trace": [],
        }
    )

    assert "cannot recommend a scheme" in result["final_answer"]
    assert "Choose Net Accounting" not in result["final_answer"]


def test_incomplete_planning_evidence_prevents_capacity_judgment():
    result = safety_agent(
        {
            "intent": "solar_planning",
            "entities": {
                "energy_kwh": 450.0,
                "capacity_kw": 5.0,
            },
            "selected_agents": [
                "energy",
                "knowledge",
                "financial",
            ],
            "knowledge_result": {
                "result_count": 0,
                "context": "",
            },
            "financial_result": {
                "financial_calculation_ready": False,
            },
            "sources": [],
            "draft_answer": "A 5 kW system is insufficient.",
            "trace": [],
        }
    )

    assert (
        "cannot determine whether that capacity is suitable"
        in result["final_answer"]
    )
    assert "is insufficient" not in result["final_answer"]


def test_preliminary_financial_output_prevents_payback_claim():
    result = safety_agent(
        {
            "intent": "financial",
            "entities": {},
            "selected_agents": ["energy", "financial", "knowledge"],
            "financial_result": {
                "financial_calculation_ready": False,
            },
            "sources": [],
            "draft_answer": "Your payback period will be five years.",
            "trace": [],
        }
    )

    answer = result["final_answer"]

    assert "cannot determine system suitability" in answer
    assert "savings or payback" in answer
    assert "five years" not in answer


def test_agentic_api_preserves_schema_for_missing_solar_metrics(
    monkeypatch,
):
    class MissingMetricsGraph:
        def invoke(self, initial_state):
            return safety_agent(
                {
                    **initial_state,
                    "selected_agents": ["energy", "knowledge"],
                    "energy_result": {
                        "latest_generation_kwh": None,
                        "generation_change_percent": None,
                    },
                    "knowledge_result": {
                        "result_count": 0,
                        "context": "",
                    },
                    "sources": [],
                    "draft_answer": (
                        "None kWh confirms a measured decrease."
                    ),
                }
            )

    monkeypatch.setattr(
        assistant,
        "build_agent_graph",
        lambda db: MissingMetricsGraph(),
    )
    monkeypatch.setattr(
        assistant,
        "analyze_text",
        lambda message: {
            "normalized_query": message.lower(),
            "intent": "solar_performance",
            "entities": {},
        },
    )
    monkeypatch.setattr(
        assistant,
        "create_audit_log",
        lambda **kwargs: None,
    )

    app.dependency_overrides[get_db] = lambda: None
    app.dependency_overrides[get_current_user] = lambda: SimpleNamespace(
        id=1
    )

    try:
        response = TestClient(app).post(
            "/api/v1/assistant/agentic",
            json={
                "message": "Why has my solar generation dropped?",
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200

    data = response.json()

    assert set(data) == {
        "message",
        "intent",
        "entities",
        "normalized_query",
        "selected_agents",
        "energy_result",
        "weather_result",
        "knowledge_result",
        "financial_result",
        "sources",
        "safety_passed",
        "safety_notes",
        "trace",
    }
    assert "No solar-generation records" in data["message"]
    assert "None kWh" not in data["message"]
    assert "measured decrease" not in data["message"]
