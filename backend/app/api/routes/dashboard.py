from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.api.deps import db_session
from app.core.security import Role, require_role
from app.models.entities import Project, Risk, Task, TaskStatus

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/analytics")
def analytics(
    project_id: int,
    session: Session = Depends(db_session),
    role: Role = Depends(require_role({Role.ADMIN, Role.PROJECT_MANAGER, Role.TEAM_LEAD, Role.STAKEHOLDER, Role.TEAM_MEMBER})),
):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    tasks = session.exec(select(Task).where(Task.project_id == project_id)).all()
    risks = session.exec(select(Risk).where(Risk.project_id == project_id)).all()

    total = len(tasks)
    done = sum(1 for task in tasks if task.status == TaskStatus.DONE)
    blocked = sum(1 for task in tasks if task.status == TaskStatus.BLOCKED)
    in_progress = sum(1 for task in tasks if task.status == TaskStatus.IN_PROGRESS)

    return {
        "project_id": project_id,
        "project_name": project.name,
        "task_metrics": {
            "total": total,
            "done": done,
            "blocked": blocked,
            "in_progress": in_progress,
            "completion_percent": int((done / total) * 100) if total else 0,
        },
        "risk_metrics": {
            "total": len(risks),
            "high_or_critical": len([r for r in risks if str(r.severity) in {"high", "critical"}]),
        },
    }
