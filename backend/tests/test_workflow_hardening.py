from app.agents.resource_allocation_agent import ResourceAllocationAgent
from app.models.entities import Project
from app.workflows import project_workflow


def test_workflow_returns_status_and_errors(session):
    project = Project(name="Phase10 Base", goal="Validate workflow hardening behavior")
    session.add(project)
    session.commit()
    session.refresh(project)

    result = project_workflow.run_project_workflow(session, project, cadence="daily")

    assert result["status"] in {"ok", "degraded", "failed"}
    assert "errors" in result
    assert isinstance(result["errors"], list)


def test_workflow_degrades_when_step_fails(monkeypatch, session):
    project = Project(name="Phase10 Fallback", goal="Force allocation failure and expect fallback")
    session.add(project)
    session.commit()
    session.refresh(project)

    def fail_allocation(*_args, **_kwargs):
        raise RuntimeError("forced allocation failure")

    monkeypatch.setattr(ResourceAllocationAgent, "run", fail_allocation)
    project_workflow._WORKFLOW = project_workflow.build_project_workflow()

    result = project_workflow.run_project_workflow(session, project, cadence="daily")

    assert result["status"] == "degraded"
    assert any(err.get("step") == "allocation" for err in result.get("errors", []))