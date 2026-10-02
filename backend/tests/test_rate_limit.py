from types import SimpleNamespace
from unittest.mock import Mock, patch

from fastapi.testclient import TestClient

from app.core.database import get_db
from app.main import app
from app.security.dependencies import get_current_user
from app.security.rate_limit import limiter


def test_agentic_endpoint_is_limited_to_twenty_requests_per_minute():
    graph = Mock()
    graph.invoke.return_value = {
        "final_answer": "Solar energy response.",
        "intent": "general",
        "entities": {},
        "normalized_query": "Explain solar energy.",
        "selected_agents": [],
        "sources": [],
        "safety_passed": True,
        "safety_notes": [],
        "trace": [],
    }

    app.dependency_overrides[get_db] = lambda: None
    app.dependency_overrides[get_current_user] = lambda: SimpleNamespace(
        id=1
    )
    limiter.reset()

    try:
        with (
            patch(
                "app.api.routes.assistant.build_agent_graph",
                return_value=graph,
            ),
            patch(
                "app.api.routes.assistant.create_audit_log"
            ),
            TestClient(app) as client,
        ):
            responses = [
                client.post(
                    "/api/v1/assistant/agentic",
                    json={
                        "message": "Explain solar energy."
                    },
                )
                for _ in range(21)
            ]
    finally:
        limiter.reset()
        app.dependency_overrides.clear()

    assert all(
        response.status_code == 200
        for response in responses[:20]
    )
    assert responses[20].status_code == 429
    assert responses[20].json()["error"].startswith(
        "Rate limit exceeded"
    )
    assert responses[20].headers[
        "X-Content-Type-Options"
    ] == "nosniff"
