from datetime import UTC, datetime
import json
import httpx
from sqlmodel import Session, select
from app.models.entities import Project, Task, Risk, Report
from app.core.config import get_settings


def generate_report(session: Session, project_id: int, cadence: str = "daily") -> Report:
    project = session.get(Project, project_id)
    tasks = session.exec(select(Task).where(Task.project_id == project_id)).all()
    risks = session.exec(select(Risk).where(Risk.project_id == project_id)).all()

    done = sum(1 for t in tasks if str(t.status) == "done")
    blocked = sum(1 for t in tasks if str(t.status) == "blocked")
    summary = (
        f"Project: {project.name}\n"
        f"Generated: {datetime.now(UTC).isoformat()}\n"
        f"Total tasks: {len(tasks)}\n"
        f"Completed: {done}\n"
        f"Blocked: {blocked}\n"
        f"Risks: {len(risks)}\n"
    )

    snapshot = {
        "project_id": project_id,
        "cadence": cadence,
        "task_count": len(tasks),
        "risk_count": len(risks),
    }

    report = Report(project_id=project_id, cadence=cadence, content=summary, snapshot_json=str(snapshot))
    session.add(report)
    session.commit()
    session.refresh(report)
    return report


def send_notification_stub(channel: str, report: Report) -> dict:
    settings = get_settings()
    if settings.notification_webhook_url.strip():
        payload = {
            "channel": channel,
            "report_id": report.id,
            "cadence": report.cadence,
            "content": report.content,
            "snapshot": report.snapshot_json,
        }
        try:
            with httpx.Client(timeout=settings.notification_timeout_seconds) as client:
                response = client.post(
                    settings.notification_webhook_url,
                    headers={"Content-Type": "application/json"},
                    content=json.dumps(payload),
                )
                response.raise_for_status()
            return {
                "sent": True,
                "channel": channel,
                "report_id": report.id,
                "message": "Notification dispatched via webhook",
            }
        except Exception as exc:
            return {
                "sent": False,
                "channel": channel,
                "report_id": report.id,
                "message": f"Webhook notification failed: {exc}",
            }

    return {
        "sent": True,
        "channel": channel,
        "report_id": report.id,
        "message": "Notification dispatched in sandbox mode",
    }
