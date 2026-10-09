from fastapi.testclient import TestClient

from app.main import app
from tests.conftest import auth_headers


client = TestClient(app)


def test_admin_settings_get_put() -> None:
    get_response = client.get("/api/v1/admin/settings")
    assert get_response.status_code == 200

    put_response = client.put(
        "/api/v1/admin/settings",
        headers=auth_headers("admin"),
        json={
            "report_cadence": "weekly",
            "escalation_hours": 6,
            "high_risk_threshold": 3,
        },
    )
    assert put_response.status_code == 200
    payload = put_response.json()
    assert payload["report_cadence"] == "weekly"
    assert payload["escalation_hours"] == 6
    assert payload["high_risk_threshold"] == 3


def test_admin_settings_forbidden_for_team_member() -> None:
    response = client.put(
        "/api/v1/admin/settings",
        headers=auth_headers("team_member"),
        json={
            "report_cadence": "daily",
            "escalation_hours": 4,
            "high_risk_threshold": 2,
        },
    )
    assert response.status_code == 403
