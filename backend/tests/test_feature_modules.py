from app.models.entities import Project, Resource, Task, TaskStatus
from app.services import allocation, communication, planning, progress, risk


def _create_project(session, name: str = "Feature Module Validation") -> Project:
    project = Project(name=name, goal="Validate feature module unit behavior")
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


def test_planning_generates_project_tasks(session) -> None:
    project = _create_project(session, name="Planning Unit Test")
    tasks = planning.generate_plan(session, project)

    assert len(tasks) >= 5
    assert all(task.project_id == project.id for task in tasks)
    assert all(task.milestone for task in tasks)


def test_allocation_assigns_owners(session) -> None:
    project = _create_project(session, name="Allocation Unit Test")
    tasks = planning.generate_plan(session, project)

    resources = [
        Resource(name="Backend One", role="backend engineer", skills_csv="python,api,sql", availability_percent=80),
        Resource(name="Frontend One", role="frontend engineer", skills_csv="react,typescript,ui", availability_percent=75),
    ]
    for resource in resources:
        session.add(resource)
    session.commit()

    assigned_tasks = allocation.allocate_tasks(session, project.id)

    assert len(assigned_tasks) == len(tasks)
    assert any(task.owner_id is not None for task in assigned_tasks)


def test_progress_computes_completion_and_blocked_counts(session) -> None:
    project = _create_project(session, name="Progress Unit Test")
    tasks = planning.generate_plan(session, project)

    tasks[0].status = TaskStatus.DONE
    tasks[1].status = TaskStatus.BLOCKED
    session.add(tasks[0])
    session.add(tasks[1])
    session.commit()

    snapshot = progress.compute_progress(session, project.id)

    assert snapshot["total"] == len(tasks)
    assert snapshot["blocked_tasks"] >= 1
    assert snapshot["completion_percent"] >= 0


def test_risk_assessment_generates_entries(session) -> None:
    project = _create_project(session, name="Risk Unit Test")
    tasks = planning.generate_plan(session, project)

    tasks[0].status = TaskStatus.BLOCKED
    session.add(tasks[0])
    session.commit()

    risks = risk.assess_risks(session, project.id)

    assert len(risks) >= 1
    assert all(entry.project_id == project.id for entry in risks)


def test_communication_generates_report_and_notification(session) -> None:
    project = _create_project(session, name="Communication Unit Test")
    planning.generate_plan(session, project)
    risk.assess_risks(session, project.id)

    report = communication.generate_report(session, project.id, cadence="daily")
    notification = communication.send_notification_stub("email", report)

    assert report.project_id == project.id
    assert report.cadence == "daily"
    assert "Project:" in report.content
    assert notification["report_id"] == report.id
    assert "sent" in notification
