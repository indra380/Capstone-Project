from __future__ import annotations

from typing import Any

from sqlmodel import Session

from app.agents.base import BaseAgent
from app.models.entities import Project
from app.services.risk import assess_risks


class RiskAssessmentAgent(BaseAgent):
    name = "risk_assessment"

    def run(self, session: Session, project: Project) -> dict[str, Any]:
        risks = assess_risks(session, project.id)
        insight = self.analyze(
            "risk_assessment_agent_prompt.md",
            {
                "project_name": project.name,
                "risk_count": len(risks),
            },
        )
        return {"risk_entries": risks, "risk_insight": insight}
