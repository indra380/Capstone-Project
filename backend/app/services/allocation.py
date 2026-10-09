from sqlmodel import Session, select
from app.models.entities import Task, Resource


def _score_resource(task: Task, resource: Resource) -> int:
    score = 0
    text = f"{task.title} {task.description}".lower()
    role_text = resource.role.lower()
    skills = [s.strip().lower() for s in resource.skills_csv.split(",") if s.strip()]

    for token in skills:
        if token in text:
            score += 3
    if any(word in role_text for word in ["lead", "manager"]) and "plan" in text:
        score += 2
    if "frontend" in text and "frontend" in role_text:
        score += 2
    if "qa" in text and "qa" in role_text:
        score += 2

    score += max(0, int(resource.availability_percent / 20))
    return score


def allocate_tasks(session: Session, project_id: int) -> list[Task]:
    tasks = session.exec(select(Task).where(Task.project_id == project_id)).all()
    resources = session.exec(select(Resource)).all()
    if not resources:
        return tasks

    for idx, task in enumerate(tasks):
        owner = max(resources, key=lambda item: (_score_resource(task, item), -idx))
        task.owner_id = owner.id
    session.commit()
    for task in tasks:
        session.refresh(task)
    return tasks
