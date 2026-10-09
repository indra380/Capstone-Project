from sqlmodel import Session
from app.models.entities import AuditLog


def log_action(
    session: Session,
    actor_role: str,
    action: str,
    entity_type: str,
    entity_id: str,
    rationale: str = "",
    actor_user_id: int | None = None,
    ip_address: str = "",
) -> AuditLog:
    entry = AuditLog(
        actor_role=actor_role,
        actor_user_id=actor_user_id,
        ip_address=ip_address,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        rationale=rationale,
    )
    session.add(entry)
    session.commit()
    session.refresh(entry)
    return entry
