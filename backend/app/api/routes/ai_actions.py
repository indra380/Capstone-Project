from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.api.deps import db_session
from app.core.security import Role, require_role
from app.models.entities import Project
from app.schemas.api import AIProjectRequest, AIStatusReportRequest
from app.services import allocation, audit, communication, planning, risk as risk_service, supervisor

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/generate-project-plan")
def generate_project_plan(
    payload: AIProjectRequest,
    session: Session = Depends(db_session),
    role: Role = Depends(require_role({Role.ADMIN, Role.PROJECT_MANAGER, Role.TEAM_LEAD})),
):
    project = session.get(Project, payload.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    tasks = planning.generate_plan(session, project)
    audit.log_action(
        session,
        actor_role=role.value,
        action="ai_plan_generated",
        entity_type="project",
        entity_id=str(project.id),
        rationale="AI planning endpoint invoked",
    )
    return {"project_id": project.id, "task_count": len(tasks), "tasks": tasks}


@router.post("/allocate-resources")
def allocate_resources(
    payload: AIProjectRequest,
    session: Session = Depends(db_session),
    role: Role = Depends(require_role({Role.ADMIN, Role.PROJECT_MANAGER, Role.TEAM_LEAD})),
):
    project = session.get(Project, payload.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    tasks = allocation.allocate_tasks(session, project.id)
    audit.log_action(
        session,
        actor_role=role.value,
        action="ai_allocation_executed",
        entity_type="project",
        entity_id=str(project.id),
        rationale="AI resource allocation endpoint invoked",
    )
    return {"project_id": project.id, "assigned_tasks": tasks}


@router.post("/risk-assessment")
def risk_assessment(
    payload: AIProjectRequest,
    session: Session = Depends(db_session),
    role: Role = Depends(require_role({Role.ADMIN, Role.PROJECT_MANAGER, Role.TEAM_LEAD})),
):
    project = session.get(Project, payload.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    risks = risk_service.assess_risks(session, project.id)
    audit.log_action(
        session,
        actor_role=role.value,
        action="ai_risk_assessed",
        entity_type="project",
        entity_id=str(project.id),
        rationale="AI risk assessment endpoint invoked",
    )
    return {"project_id": project.id, "risks": risks}


@router.post("/generate-status-report")
def generate_status_report(
    payload: AIStatusReportRequest,
    session: Session = Depends(db_session),
    role: Role = Depends(require_role({Role.ADMIN, Role.PROJECT_MANAGER, Role.TEAM_LEAD, Role.STAKEHOLDER})),
):
    project = session.get(Project, payload.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    report = communication.generate_report(session, project.id, cadence=payload.cadence)
    audit.log_action(
        session,
        actor_role=role.value,
        action="ai_status_report_generated",
        entity_type="project",
        entity_id=str(project.id),
        rationale="AI status report endpoint invoked",
    )
    return {"project_id": project.id, "report": report}


@router.post("/run-supervisor")
def run_supervisor(
    payload: AIStatusReportRequest,
    session: Session = Depends(db_session),
    role: Role = Depends(require_role({Role.ADMIN, Role.PROJECT_MANAGER})),
):
    project = session.get(Project, payload.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    orchestration = supervisor.run_goal_to_report(session, project, cadence=payload.cadence)
    audit.log_action(
        session,
        actor_role=role.value,
        action="supervisor_orchestration_run",
        entity_type="project",
        entity_id=str(project.id),
        rationale="Supervisor orchestration endpoint invoked",
    )
    return {"project_id": project.id, "orchestration": orchestration}
