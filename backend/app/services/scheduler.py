from __future__ import annotations

from apscheduler.schedulers.background import BackgroundScheduler
from sqlmodel import select

from app.core.config import get_settings
from app.db.session import Session, engine
from app.models.entities import Project
from app.services import communication

scheduler = BackgroundScheduler()


def _scheduled_reports_job() -> None:
    settings = get_settings()
    with Session(engine) as session:
        projects = session.exec(select(Project)).all()
        for project in projects:
            communication.generate_report(
                session,
                project.id,
                cadence=settings.default_report_cadence,
            )


def start_scheduler() -> None:
    if scheduler.running:
        return
    settings = get_settings()
    scheduler.add_job(
        _scheduled_reports_job,
        trigger="interval",
        minutes=settings.scheduler_interval_minutes,
        id="scheduled_reports",
        replace_existing=True,
    )
    scheduler.start()


def stop_scheduler() -> None:
    if scheduler.running:
        scheduler.shutdown(wait=False)
