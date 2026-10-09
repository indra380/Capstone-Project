from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.api.deps import db_session
from app.core.security import Role, require_role
from app.models.entities import Risk, RiskSeverity
from app.schemas.api import RiskCreateRequest, RiskUpdateRequest
from app.services import audit

router = APIRouter(prefix="/risks", tags=["risks"])


@router.post("", status_code=201)
def create_risk(
    payload: RiskCreateRequest,
    session: Session = Depends(db_session),
    role: Role = Depends(require_role({Role.ADMIN, Role.PROJECT_MANAGER, Role.TEAM_LEAD})),
):
    risk = Risk(
        project_id=payload.project_id,
        title=payload.title,
        severity=RiskSeverity(payload.severity),
        mitigation=payload.mitigation,
    )
    session.add(risk)
    session.commit()
    session.refresh(risk)
    audit.log_action(
        session,
        actor_role=role.value,
        action="risk_created",
        entity_type="project",
        entity_id=str(risk.project_id),
        rationale=f"Risk {risk.id} created via API",
    )
    return risk


@router.get("")
def list_risks(
    project_id: int | None = None,
    session: Session = Depends(db_session),
    role: Role = Depends(require_role({Role.ADMIN, Role.PROJECT_MANAGER, Role.TEAM_LEAD, Role.TEAM_MEMBER, Role.STAKEHOLDER})),
):
    query = select(Risk)
    if project_id is not None:
        query = query.where(Risk.project_id == project_id)
    return session.exec(query).all()


@router.get("/{risk_id}")
def get_risk(
    risk_id: int,
    session: Session = Depends(db_session),
    role: Role = Depends(require_role({Role.ADMIN, Role.PROJECT_MANAGER, Role.TEAM_LEAD, Role.TEAM_MEMBER, Role.STAKEHOLDER})),
):
    risk = session.get(Risk, risk_id)
    if not risk:
        raise HTTPException(status_code=404, detail="Risk not found")
    return risk


@router.put("/{risk_id}")
def update_risk(
    risk_id: int,
    payload: RiskUpdateRequest,
    session: Session = Depends(db_session),
    role: Role = Depends(require_role({Role.ADMIN, Role.PROJECT_MANAGER, Role.TEAM_LEAD})),
):
    risk = session.get(Risk, risk_id)
    if not risk:
        raise HTTPException(status_code=404, detail="Risk not found")

    data = payload.model_dump(exclude_unset=True)
    if "severity" in data and data["severity"] is not None:
        data["severity"] = RiskSeverity(data["severity"])

    for key, value in data.items():
        setattr(risk, key, value)

    session.add(risk)
    session.commit()
    session.refresh(risk)
    audit.log_action(
        session,
        actor_role=role.value,
        action="risk_updated",
        entity_type="project",
        entity_id=str(risk.project_id),
        rationale=f"Risk {risk.id} updated via API",
    )
    return risk


@router.delete("/{risk_id}", status_code=204)
def delete_risk(
    risk_id: int,
    session: Session = Depends(db_session),
    role: Role = Depends(require_role({Role.ADMIN, Role.PROJECT_MANAGER})),
):
    risk = session.get(Risk, risk_id)
    if not risk:
        raise HTTPException(status_code=404, detail="Risk not found")
    risk_id = risk.id
    project_id = risk.project_id
    session.delete(risk)
    session.commit()
    audit.log_action(
        session,
        actor_role=role.value,
        action="risk_deleted",
        entity_type="project",
        entity_id=str(project_id),
        rationale=f"Risk {risk_id} deleted via API",
    )
    return None
