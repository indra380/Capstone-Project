from fastapi.testclient import TestClient

from app.main import app
from tests.conftest import auth_headers


client = TestClient(app)


def _create_project() -> int:
    response = client.post(
        "/api/v1/projects",
        headers=auth_headers("project_manager"),
        json={
            "name": "Capstone Validation Project",
            "goal": "Launch AI PM system in 2 weeks with quality gates and stakeholder reporting",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert "project_id" in data
    return data["project_id"]


def test_create_project_and_overview() -> None:
    project_id = _create_project()

    overview = client.get(
        f"/api/v1/projects/{project_id}/overview",
        headers=auth_headers("team_member"),
    )
    assert overview.status_code == 200
    payload = overview.json()
    assert payload["project_id"] == project_id
    assert "completion_percent" in payload
    assert "ai_summary" in payload


def test_task_update_risk_report_export_and_audit() -> None:
    project_id = _create_project()

    tasks_response = client.get(
        f"/api/v1/projects/{project_id}/tasks",
        headers=auth_headers("team_member"),
    )
    assert tasks_response.status_code == 200
    tasks = tasks_response.json()
    assert len(tasks) > 0

    task_id = tasks[0]["id"]

    patch_response = client.patch(
        f"/api/v1/projects/{project_id}/tasks/{task_id}",
        headers=auth_headers("team_member"),
        json={"status": "in_progress", "reason": "Started implementation"},
    )
    assert patch_response.status_code == 200

    override_response = client.post(
        f"/api/v1/projects/{project_id}/override",
        headers=auth_headers("project_manager"),
        json={"task_id": task_id, "owner_id": 1, "rationale": "Load balancing"},
    )
    assert override_response.status_code == 200

    report_response = client.post(
        f"/api/v1/projects/{project_id}/reports",
        headers=auth_headers("team_lead"),
    )
    assert report_response.status_code == 200
    assert report_response.json()["notification"]["sent"] in [True, False]

    export_json = client.get(
        f"/api/v1/projects/{project_id}/export?format=json",
        headers=auth_headers("stakeholder"),
    )
    assert export_json.status_code == 200
    assert "project" in export_json.json()

    export_csv = client.get(
        f"/api/v1/projects/{project_id}/export?format=csv",
        headers=auth_headers("stakeholder"),
    )
    assert export_csv.status_code == 200
    assert export_csv.headers["content-type"].startswith("text/csv")

    audit_response = client.get(
        f"/api/v1/projects/{project_id}/audit",
        headers=auth_headers("project_manager"),
    )
    assert audit_response.status_code == 200


def test_projects_requires_auth() -> None:
    response = client.get("/api/v1/projects")
    assert response.status_code == 401


def test_projects_forbids_unauthorized_role() -> None:
    response = client.post(
        "/api/v1/projects",
        headers=auth_headers("stakeholder"),
        json={
            "name": "Unauthorized Create Attempt",
            "goal": "This should fail due to role guard",
        },
    )
    assert response.status_code == 403
