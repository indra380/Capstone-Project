from sqlmodel import Session
from app.models.entities import Task, Project


def generate_plan(session: Session, project: Project) -> list[Task]:
    templates = [
        ("Requirements Finalization", "Lock scope and constraints", 2, "M1"),
        ("Architecture and Scaffolding", "Baseline architecture and setup", 2, "M2"),
        ("Core Feature Build", "Implement planning, allocation, tracking", 4, "M3"),
        ("Risk and Communication", "Risk scoring and updates", 2, "M4"),
        ("Integration and QA", "System hardening and tests", 3, "M5"),
        ("UAT and Demo Prep", "Finalize demo and docs", 2, "M6"),
    ]

    created: list[Task] = []
    for title, description, duration, milestone in templates:
        task = Task(
            project_id=project.id,
            title=title,
            description=description,
            duration_days=duration,
            milestone=milestone,
        )
        session.add(task)
        session.flush()
        created.append(task)

    for idx, task in enumerate(created):
        if idx > 0:
            task.depends_on_csv = str(created[idx - 1].id)
    session.commit()
    for task in created:
        session.refresh(task)
    return created
