from sqlmodel import Session, select
from app.models.entities import Risk, Task, TaskStatus, RiskSeverity


def assess_risks(session: Session, project_id: int) -> list[Risk]:
    tasks = session.exec(select(Task).where(Task.project_id == project_id)).all()
    existing = session.exec(select(Risk).where(Risk.project_id == project_id)).all()
    for risk in existing:
        session.delete(risk)
    session.flush()

    blocked = [task for task in tasks if task.status == TaskStatus.BLOCKED]
    in_progress = [task for task in tasks if task.status == TaskStatus.IN_PROGRESS]

    risks: list[Risk] = []
    if blocked:
        risks.append(
            Risk(
                project_id=project_id,
                title="Blocked tasks may impact milestones",
                severity=RiskSeverity.HIGH,
                mitigation="Escalate blockers within 4 hours and assign fallback owner",
            )
        )
    if len(in_progress) > max(3, len(tasks) // 2):
        risks.append(
            Risk(
                project_id=project_id,
                title="Too many parallel tasks can reduce throughput",
                severity=RiskSeverity.MEDIUM,
                mitigation="Limit active WIP and prioritize dependency-critical tasks",
            )
        )

    if not risks and tasks:
        risks.append(
            Risk(
                project_id=project_id,
                title="No immediate critical risk detected",
                severity=RiskSeverity.LOW,
                mitigation="Continue daily monitoring and weekly review",
            )
        )

    for risk in risks:
        session.add(risk)
    session.commit()
    for risk in risks:
        session.refresh(risk)
    return risks
