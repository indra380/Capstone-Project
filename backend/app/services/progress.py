from sqlmodel import Session, select
from app.models.entities import Task, TaskStatus


def compute_progress(session: Session, project_id: int) -> dict:
    tasks = session.exec(select(Task).where(Task.project_id == project_id)).all()
    if not tasks:
        return {"completion_percent": 0, "blocked_tasks": 0, "total": 0}

    done = sum(1 for task in tasks if task.status == TaskStatus.DONE)
    blocked = sum(1 for task in tasks if task.status == TaskStatus.BLOCKED)
    completion_percent = int((done / len(tasks)) * 100)
    return {
        "completion_percent": completion_percent,
        "blocked_tasks": blocked,
        "total": len(tasks),
    }
