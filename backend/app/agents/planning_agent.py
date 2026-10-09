from __future__ import annotations

from typing import Any

from sqlmodel import Session

from app.agents.base import BaseAgent
from app.models.entities import Project
from app.services.planning import generate_plan


class PlanningAgent(BaseAgent):
    name = "planning"

    def run(self, session: Session, project: Project) -> dict[str, Any]:
        tasks = generate_plan(session, project)
        insight = self.analyze(
            "planning_agent_prompt.md",
            {
                "project_name": project.name,
                "goal": project.goal,
                "task_count": len(tasks),
            },
        )
        return {"plan_tasks": tasks, "planning_insight": insight}
