from types import SimpleNamespace
from unittest.mock import Mock, patch

from starlette.requests import Request

from app.api.routes.assistant import (
    analyze_message,
    run_agentic_assistant,
)
from app.api.routes.assistant_stream import (
    _agentic_response,
)
from app.security.privacy import (
    redact_sensitive_data,
)


EMAIL = "customer@example.com"
TOKEN = (
    "eyJhbGciOiJIUzI1NiJ9."
    "eyJzdWIiOiIxIn0."
    "signature_123"
)


def _request(path: str) -> Request:
    return Request(
        {
            "type": "http",
            "method": "POST",
            "path": path,
            "headers": [],
            "client": ("127.0.0.1", 12345),
        }
    )


def test_redact_sensitive_data_removes_email_and_jwt():
    result = redact_sensitive_data(
        f"Contact {EMAIL} with bearer token {TOKEN}."
    )

    assert result == (
        "Contact [REDACTED_EMAIL] with bearer token "
        "[REDACTED_TOKEN]."
    )


def test_email_redaction():
    text = (
        "Contact user@example.com "
        "for information."
    )

    result = redact_sensitive_data(
        text
    )

    assert "user@example.com" not in result
    assert "[REDACTED_EMAIL]" in result


def test_redact_sensitive_data_preserves_normal_text():
    text = "A 5 kW solar system may generate renewable energy."

    assert redact_sensitive_data(text) == text


def test_analyze_endpoint_redacts_generated_output():
    client = Mock()
    client.health.return_value = True
    client.generate.return_value = f"Email {EMAIL}; token {TOKEN}"

    with patch(
        "app.api.routes.assistant.get_llm_client",
        return_value=client,
    ):
        response = analyze_message(
            request=_request("/api/v1/assistant/analyze"),
            data=SimpleNamespace(
                message="Explain solar energy."
            ),
            current_user=SimpleNamespace(id=1),
        )

    assert response.message == (
        "Email [REDACTED_EMAIL]; token [REDACTED_TOKEN]"
    )


def test_agentic_endpoint_redacts_final_answer():
    graph = Mock()
    response_db = Mock()
    graph.invoke.return_value = {
        "final_answer": f"Email {EMAIL}; token {TOKEN}",
        "intent": "general",
        "entities": {},
        "normalized_query": "Explain solar energy.",
        "selected_agents": [],
        "sources": [],
        "safety_passed": True,
        "safety_notes": [],
        "trace": [],
    }

    with patch(
        "app.api.routes.assistant.build_agent_graph",
        return_value=graph,
    ), patch(
        "app.api.routes.assistant.create_audit_log"
    ) as audit_log:
        response = run_agentic_assistant(
            request=_request("/api/v1/assistant/agentic"),
            data=SimpleNamespace(
                message="Explain solar energy."
            ),
            db=response_db,
            current_user=SimpleNamespace(id=1),
        )

    assert response.message == (
        "Email [REDACTED_EMAIL]; token [REDACTED_TOKEN]"
    )
    audit_log.assert_called_once_with(
        db=response_db,
        user_id=1,
        action="agentic_assistant_request",
        status="success",
        resource="assistant",
    )


def test_streaming_response_redacts_final_answer():
    response = _agentic_response(
        {
            "final_answer": f"Email {EMAIL}; token {TOKEN}",
            "intent": "general",
            "entities": {},
            "selected_agents": [],
            "sources": [],
            "safety_passed": True,
            "safety_notes": [],
            "trace": [],
        },
        fallback_query="Explain solar energy.",
    )

    assert response.message == (
        "Email [REDACTED_EMAIL]; token [REDACTED_TOKEN]"
    )
