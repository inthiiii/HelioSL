from sqlalchemy.orm import Session

from app.models.audit import AuditLog


def create_audit_log(
    db: Session,
    action: str,
    status: str,
    user_id: int | None = None,
    resource: str | None = None,
) -> AuditLog:

    log = AuditLog(
        user_id=user_id,
        action=action,
        status=status,
        resource=resource,
    )

    db.add(log)
    db.commit()
    db.refresh(log)

    return log
