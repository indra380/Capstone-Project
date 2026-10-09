from __future__ import annotations

from typing import Any

from sqlmodel import Session

from app.agents.base import BaseAgent
from app.models.entities import Project
from app.services.progress import compute_progress


class ProgressTrackingAgent(BaseAgent):
    name = "progress_tracking"

    def run(self, session: Session, project: Project) -> dict[str, Any]:
        snapshot = compute_progress(session, project.id)
        insight = self.analyze(
            "progress_tracking_agent_prompt.md",
            {
                "project_name": project.name,
                "completion_percent": snapshot.get("completion_percent", 0),
                "blocked_tasks": snapshot.get("blocked_tasks", 0),
            },
        )
        return {"progress_snapshot": snapshot, "progress_insight": insight}
