from sqlmodel import Session, select
from app.core.exceptions import AppException
from app.models.entities import Project, Resource, Task, Risk
from app.schemas.domain import ResourceIn
from app.services import progress
from app.workflows import run_project_workflow


def bootstrap_resources(session: Session, resources: list[ResourceIn]) -> list[Resource]:
    existing = session.exec(select(Resource)).all()
    if existing:
        return list(existing)

    created: list[Resource] = []
    for item in resources:
        record = Resource(
            name=item.name,
            role=item.role,
            skills_csv=",".join(item.skills),
            availability_percent=item.availability_percent,
        )
        session.add(record)
        session.flush()
        created.append(record)
    session.commit()
    return created


def run_goal_to_report(session: Session, project: Project, cadence: str = "daily") -> dict:
    if project.id is None:
        raise AppException(message="Project must be persisted before orchestration", code="PROJECT_NOT_PERSISTED")

    try:
        return run_project_workflow(session, project, cadence=cadence)
    except Exception as exc:
        raise AppException(
            message=f"Supervisor orchestration failed: {exc}",
            code="WORKFLOW_EXECUTION_FAILED",
            status_code=500,
        ) from exc


def get_project_overview(session: Session, project_id: int) -> dict:
    project = session.get(Project, project_id)
    if project is None:
        raise AppException(message="Project not found", code="PROJECT_NOT_FOUND", status_code=404)

    tasks = session.exec(select(Task).where(Task.project_id == project_id)).all()
    risks = session.exec(select(Risk).where(Risk.project_id == project_id)).all()
    progress_snapshot = progress.compute_progress(session, project_id)
    return {
        "project_id": project.id,
        "project_name": project.name,
        "completion_percent": progress_snapshot["completion_percent"],
        "blocked_tasks": progress_snapshot["blocked_tasks"],
        "high_risks": len([r for r in risks if r.severity in {"high", "critical"}]),
        "report_cadence": "daily",
        "task_count": len(tasks),
    }
