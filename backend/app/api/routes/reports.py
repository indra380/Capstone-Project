from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.api.deps import db_session
from app.core.security import Role, require_role
from app.models.entities import Project, Report
from app.schemas.api import GenerateReportRequest
from app.services.communication import generate_report, send_notification_stub

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("")
def list_reports(
    project_id: int | None = None,
    session: Session = Depends(db_session),
    role: Role = Depends(require_role({Role.ADMIN, Role.PROJECT_MANAGER, Role.TEAM_LEAD, Role.STAKEHOLDER, Role.TEAM_MEMBER})),
):
    query = select(Report)
    if project_id is not None:
        query = query.where(Report.project_id == project_id)
    return session.exec(query).all()


@router.get("/{report_id}")
def get_report(
    report_id: int,
    session: Session = Depends(db_session),
    role: Role = Depends(require_role({Role.ADMIN, Role.PROJECT_MANAGER, Role.TEAM_LEAD, Role.STAKEHOLDER, Role.TEAM_MEMBER})),
):
    report = session.get(Report, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report


@router.post("/generate")
def generate_report_endpoint(
    payload: GenerateReportRequest,
    session: Session = Depends(db_session),
    role: Role = Depends(require_role({Role.ADMIN, Role.PROJECT_MANAGER, Role.TEAM_LEAD})),
):
    project = session.get(Project, payload.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    report = generate_report(session, payload.project_id, cadence=payload.cadence)
    notification = send_notification_stub(payload.channel, report)
    return {"report": report, "notification": notification}
