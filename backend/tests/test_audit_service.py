from unittest.mock import Mock

from app.models.audit import AuditLog
from app.services.audit_service import (
    create_audit_log,
)


def test_create_audit_log_records_only_audit_metadata():
    db = Mock()

    result = create_audit_log(
        db=db,
        user_id=42,
        action="agentic_assistant_request",
        status="success",
        resource="assistant",
    )

    assert isinstance(result, AuditLog)
    assert result.user_id == 42
    assert result.action == "agentic_assistant_request"
    assert result.status == "success"
    assert result.resource == "assistant"
    assert not hasattr(result, "prompt")
    assert not hasattr(result, "password")
    assert not hasattr(result, "token")
    db.add.assert_called_once_with(result)
    db.commit.assert_called_once_with()
    db.refresh.assert_called_once_with(result)
