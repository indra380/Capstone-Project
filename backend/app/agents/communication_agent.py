from __future__ import annotations

from typing import Any

from sqlmodel import Session

from app.agents.base import BaseAgent
from app.models.entities import Project
from app.services.communication import generate_report


class CommunicationAgent(BaseAgent):
    name = "communication"

    def run(self, session: Session, project: Project, cadence: str = "daily") -> dict[str, Any]:
        report = generate_report(session, project.id, cadence=cadence)
        insight = self.analyze(
            "communication_agent_prompt.md",
            {
                "project_name": project.name,
                "cadence": cadence,
                "report_id": report.id,
            },
        )
        return {"report": report, "communication_insight": insight}
