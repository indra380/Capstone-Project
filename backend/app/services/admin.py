from datetime import UTC, datetime
from sqlmodel import Session, select
from app.models.entities import SystemSetting


DEFAULTS = {
    "report_cadence": "daily",
    "escalation_hours": "4",
    "high_risk_threshold": "2",
}


def get_settings(session: Session) -> dict:
    rows = session.exec(select(SystemSetting)).all()
    values = DEFAULTS.copy()
    for row in rows:
        values[row.key] = row.value
    return {
        "report_cadence": values["report_cadence"],
        "escalation_hours": int(values["escalation_hours"]),
        "high_risk_threshold": int(values["high_risk_threshold"]),
    }


def upsert_settings(session: Session, payload: dict) -> dict:
    for key, value in payload.items():
        row = session.exec(select(SystemSetting).where(SystemSetting.key == key)).first()
        if row is None:
            row = SystemSetting(key=key, value=str(value), updated_at=datetime.now(UTC))
            session.add(row)
        else:
            row.value = str(value)
            row.updated_at = datetime.now(UTC)
            session.add(row)
    session.commit()
    return get_settings(session)
