from fastapi.testclient import TestClient

from app.main import app
from tests.conftest import auth_headers


client = TestClient(app)


def _create_project() -> int:
    response = client.post(
        "/api/v1/projects",
        headers=auth_headers("project_manager"),
        json={
            "name": "Governance Validation Project",
            "goal": "Validate RBAC and audit controls",
        },
    )
    assert response.status_code == 201
    return response.json()["project_id"]


def test_ai_actions_and_risk_actions_are_audited() -> None:
    project_id = _create_project()

    plan_response = client.post(
        "/api/v1/ai/generate-project-plan",
        headers=auth_headers("project_manager"),
        json={"project_id": project_id},
    )
    assert plan_response.status_code == 200

    allocation_response = client.post(
        "/api/v1/ai/allocate-resources",
        headers=auth_headers("project_manager"),
        json={"project_id": project_id},
    )
    assert allocation_response.status_code == 200

    risk_assessment_response = client.post(
        "/api/v1/ai/risk-assessment",
        headers=auth_headers("project_manager"),
        json={"project_id": project_id},
    )
    assert risk_assessment_response.status_code == 200

    create_risk_response = client.post(
        "/api/v1/risks",
        headers=auth_headers("project_manager"),
        json={
            "project_id": project_id,
            "title": "Vendor delay",
            "severity": "high",
            "mitigation": "Prepare alternate supplier",
        },
    )
    assert create_risk_response.status_code == 201
    risks_response = client.get(
        f"/api/v1/risks?project_id={project_id}",
        headers=auth_headers("project_manager"),
    )
    assert risks_response.status_code == 200
    risks_payload = risks_response.json()
    assert len(risks_payload) > 0
    risk_id = risks_payload[-1]["id"]

    update_risk_response = client.put(
        f"/api/v1/risks/{risk_id}",
        headers=auth_headers("project_manager"),
        json={"mitigation": "Use buffer plan and alternate supplier"},
    )
    assert update_risk_response.status_code == 200

    delete_risk_response = client.delete(
        f"/api/v1/risks/{risk_id}",
        headers=auth_headers("project_manager"),
    )
    assert delete_risk_response.status_code == 204

    audit_response = client.get(
        f"/api/v1/projects/{project_id}/audit",
        headers=auth_headers("project_manager"),
    )
    assert audit_response.status_code == 200
    actions = {entry["action"] for entry in audit_response.json()}

    assert "ai_plan_generated" in actions
    assert "ai_allocation_executed" in actions
    assert "ai_risk_assessed" in actions
    assert "risk_created" in actions
    assert "risk_updated" in actions
    assert "risk_deleted" in actions


def test_ai_planning_endpoint_forbidden_for_stakeholder() -> None:
    project_id = _create_project()
    response = client.post(
        "/api/v1/ai/generate-project-plan",
        headers=auth_headers("stakeholder"),
        json={"project_id": project_id},
    )
    assert response.status_code == 403