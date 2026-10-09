from io import StringIO
import csv
from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlmodel import Session, select

from app.api.deps import db_session
from app.core.security import Role, require_role
from app.models.entities import Project, Task, Risk, Report, AuditLog
from app.schemas.domain import (
    CreateProjectRequest,
    ProjectSnapshotOut,
    StatusUpdateRequest,
    OverrideRequest,
    ResourceIn,
)
from app.schemas.api import ProjectUpdateRequest
from app.services import supervisor, audit, communication, risk as risk_service

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("")
def list_projects(
    session: Session = Depends(db_session),
    role: Role = Depends(require_role({Role.ADMIN, Role.PROJECT_MANAGER, Role.TEAM_LEAD, Role.TEAM_MEMBER, Role.STAKEHOLDER})),
):
    return session.exec(select(Project)).all()


@router.get("/{project_id}")
def get_project(
    project_id: int,
    session: Session = Depends(db_session),
    role: Role = Depends(require_role({Role.ADMIN, Role.PROJECT_MANAGER, Role.TEAM_LEAD, Role.TEAM_MEMBER, Role.STAKEHOLDER})),
):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.post("", status_code=201)
def create_project(
    payload: CreateProjectRequest,
    session: Session = Depends(db_session),
    role: Role = Depends(require_role({Role.PROJECT_MANAGER, Role.ADMIN})),
):
    project = Project(name=payload.name, goal=payload.goal, deadline=payload.deadline)
    session.add(project)
    session.commit()
    session.refresh(project)

    bootstrap = [
        ResourceIn(name="Asha", role="Backend Engineer", skills=["python", "api", "sql"], availability_percent=80),
        ResourceIn(name="Rahul", role="Frontend Engineer", skills=["react", "typescript", "ui"], availability_percent=75),
        ResourceIn(name="Maya", role="QA Engineer", skills=["testing", "automation"], availability_percent=70),
        ResourceIn(name="Nikhil", role="Project Lead", skills=["planning", "communication"], availability_percent=60),
    ]
    supervisor.bootstrap_resources(session, bootstrap)
    result = supervisor.run_goal_to_report(session, project)

    audit.log_action(
        session,
        actor_role=role.value,
        action="project_created",
        entity_type="project",
        entity_id=str(project.id),
        rationale="Initial goal intake and orchestration execution",
    )

    return {"project_id": project.id, "orchestration": result}


@router.put("/{project_id}")
def update_project(
    project_id: int,
    payload: ProjectUpdateRequest,
    session: Session = Depends(db_session),
    role: Role = Depends(require_role({Role.ADMIN, Role.PROJECT_MANAGER})),
):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(project, key, value)

    session.add(project)
    session.commit()
    session.refresh(project)
    return project


@router.delete("/{project_id}", status_code=204)
def delete_project(
    project_id: int,
    session: Session = Depends(db_session),
    role: Role = Depends(require_role({Role.ADMIN, Role.PROJECT_MANAGER})),
):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    session.delete(project)
    session.commit()
    return None


@router.get("/{project_id}/overview", response_model=ProjectSnapshotOut)
def overview(
    project_id: int,
    session: Session = Depends(db_session),
    role: Role = Depends(require_role({Role.ADMIN, Role.PROJECT_MANAGER, Role.TEAM_LEAD, Role.TEAM_MEMBER, Role.STAKEHOLDER})),
):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return supervisor.get_project_overview(session, project_id)


@router.get("/{project_id}/tasks")
def list_tasks(
    project_id: int,
    session: Session = Depends(db_session),
    role: Role = Depends(require_role({Role.ADMIN, Role.PROJECT_MANAGER, Role.TEAM_LEAD, Role.TEAM_MEMBER, Role.STAKEHOLDER})),
):
    return session.exec(select(Task).where(Task.project_id == project_id)).all()


@router.patch("/{project_id}/tasks/{task_id}")
def update_task_status(
    project_id: int,
    task_id: int,
    payload: StatusUpdateRequest,
    session: Session = Depends(db_session),
    role: Role = Depends(require_role({Role.ADMIN, Role.PROJECT_MANAGER, Role.TEAM_LEAD, Role.TEAM_MEMBER})),
):
    task = session.get(Task, task_id)
    if not task or task.project_id != project_id:
        raise HTTPException(status_code=404, detail="Task not found")

    task.status = payload.status
    if payload.reason:
        task.description = f"{task.description}\nReason: {payload.reason}".strip()
    session.add(task)
    session.commit()
    session.refresh(task)

    risk_service.assess_risks(session, project_id)
    return task


@router.post("/{project_id}/override")
def override_assignment(
    project_id: int,
    payload: OverrideRequest,
    session: Session = Depends(db_session),
    role: Role = Depends(require_role({Role.PROJECT_MANAGER, Role.ADMIN, Role.TEAM_LEAD})),
):
    task = session.get(Task, payload.task_id)
    if not task or task.project_id != project_id:
        raise HTTPException(status_code=404, detail="Task not found")
    task.owner_id = payload.owner_id
    session.add(task)
    session.commit()

    audit.log_action(
        session,
        actor_role=role.value,
        action="manual_override",
        entity_type="task",
        entity_id=str(payload.task_id),
        rationale=payload.rationale,
    )
    return {"ok": True, "task_id": task.id, "owner_id": task.owner_id}


@router.post("/{project_id}/reports")
def generate_report(
    project_id: int,
    channel: str = Query(default="email"),
    cadence: str = Query(default="daily"),
    session: Session = Depends(db_session),
    role: Role = Depends(require_role({Role.ADMIN, Role.PROJECT_MANAGER, Role.TEAM_LEAD})),
):
    report = communication.generate_report(session, project_id, cadence=cadence)
    notification_result = communication.send_notification_stub(channel, report)
    return {"report": report, "notification": notification_result}


@router.get("/{project_id}/risks")
def list_risks(
    project_id: int,
    session: Session = Depends(db_session),
    role: Role = Depends(require_role({Role.ADMIN, Role.PROJECT_MANAGER, Role.TEAM_LEAD, Role.TEAM_MEMBER, Role.STAKEHOLDER})),
):
    return session.exec(select(Risk).where(Risk.project_id == project_id)).all()


@router.get("/{project_id}/reports/history")
def report_history(
    project_id: int,
    session: Session = Depends(db_session),
    role: Role = Depends(require_role({Role.ADMIN, Role.PROJECT_MANAGER, Role.TEAM_LEAD, Role.TEAM_MEMBER, Role.STAKEHOLDER})),
):
    return session.exec(select(Report).where(Report.project_id == project_id)).all()


@router.get("/{project_id}/audit")
def audit_history(
    project_id: int,
    session: Session = Depends(db_session),
    role: Role = Depends(require_role({Role.ADMIN, Role.PROJECT_MANAGER, Role.TEAM_LEAD})),
):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    tasks = session.exec(select(Task).where(Task.project_id == project_id)).all()
    task_ids = {str(task.id) for task in tasks if task.id is not None}
    risks = session.exec(select(Risk).where(Risk.project_id == project_id)).all()
    risk_ids = {str(risk.id) for risk in risks if risk.id is not None}

    logs = session.exec(select(AuditLog)).all()
    return [
        log
        for log in logs
        if (log.entity_type == "project" and log.entity_id == str(project_id))
        or (log.entity_type == "task" and log.entity_id in task_ids)
        or (log.entity_type == "risk" and log.entity_id in risk_ids)
    ]


@router.get("/{project_id}/export")
def export_project_data(
    project_id: int,
    format: str = Query(default="json", pattern="^(json|csv)$"),
    session: Session = Depends(db_session),
    role: Role = Depends(require_role({Role.ADMIN, Role.PROJECT_MANAGER, Role.TEAM_LEAD, Role.STAKEHOLDER})),
):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    tasks = session.exec(select(Task).where(Task.project_id == project_id)).all()
    risks = session.exec(select(Risk).where(Risk.project_id == project_id)).all()
    payload = {
        "project": {
            "id": project.id,
            "name": project.name,
            "goal": project.goal,
            "status": project.status,
        },
        "tasks": [
            {
                "id": t.id,
                "title": t.title,
                "status": t.status,
                "owner_id": t.owner_id,
                "milestone": t.milestone,
                "duration_days": t.duration_days,
            }
            for t in tasks
        ],
        "risks": [
            {
                "id": r.id,
                "title": r.title,
                "severity": r.severity,
                "mitigation": r.mitigation,
            }
            for r in risks
        ],
    }

    if format == "json":
        return payload

    csv_buffer = StringIO()
    writer = csv.DictWriter(
        csv_buffer,
        fieldnames=["task_id", "task_title", "task_status", "owner_id", "risk_id", "risk_severity"],
    )
    writer.writeheader()
    max_rows = max(len(tasks), len(risks), 1)
    for idx in range(max_rows):
        task = tasks[idx] if idx < len(tasks) else None
        risk = risks[idx] if idx < len(risks) else None
        writer.writerow(
            {
                "task_id": getattr(task, "id", ""),
                "task_title": getattr(task, "title", ""),
                "task_status": getattr(task, "status", ""),
                "owner_id": getattr(task, "owner_id", ""),
                "risk_id": getattr(risk, "id", ""),
                "risk_severity": getattr(risk, "severity", ""),
            }
        )

    return Response(
        content=csv_buffer.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=project_{project_id}_export.csv"},
    )
