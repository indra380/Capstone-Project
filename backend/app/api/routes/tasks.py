from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.api.deps import db_session
from app.core.security import Role, require_role
from app.models.entities import Task, TaskStatus
from app.schemas.api import TaskCreateRequest, TaskUpdateRequest

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", status_code=201)
def create_task(
    payload: TaskCreateRequest,
    session: Session = Depends(db_session),
    role: Role = Depends(require_role({Role.ADMIN, Role.PROJECT_MANAGER, Role.TEAM_LEAD})),
):
    task = Task(
        project_id=payload.project_id,
        title=payload.title,
        description=payload.description,
        duration_days=payload.duration_days,
        milestone=payload.milestone,
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.get("")
def list_tasks(
    project_id: int | None = None,
    session: Session = Depends(db_session),
    role: Role = Depends(require_role({Role.ADMIN, Role.PROJECT_MANAGER, Role.TEAM_LEAD, Role.TEAM_MEMBER, Role.STAKEHOLDER})),
):
    query = select(Task)
    if project_id is not None:
        query = query.where(Task.project_id == project_id)
    return session.exec(query).all()


@router.get("/{task_id}")
def get_task(
    task_id: int,
    session: Session = Depends(db_session),
    role: Role = Depends(require_role({Role.ADMIN, Role.PROJECT_MANAGER, Role.TEAM_LEAD, Role.TEAM_MEMBER, Role.STAKEHOLDER})),
):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}")
def update_task(
    task_id: int,
    payload: TaskUpdateRequest,
    session: Session = Depends(db_session),
    role: Role = Depends(require_role({Role.ADMIN, Role.PROJECT_MANAGER, Role.TEAM_LEAD, Role.TEAM_MEMBER})),
):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    data = payload.model_dump(exclude_unset=True)
    if "status" in data and data["status"] is not None:
        data["status"] = TaskStatus(data["status"])

    for key, value in data.items():
        setattr(task, key, value)

    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.delete("/{task_id}", status_code=204)
def delete_task(
    task_id: int,
    session: Session = Depends(db_session),
    role: Role = Depends(require_role({Role.ADMIN, Role.PROJECT_MANAGER})),
):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(task)
    session.commit()
    return None
