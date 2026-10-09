from __future__ import annotations

from typing import Any

from sqlmodel import Session

from app.agents.base import BaseAgent
from app.models.entities import Project
from app.services.allocation import allocate_tasks


class ResourceAllocationAgent(BaseAgent):
    name = "resource_allocation"

    def run(self, session: Session, project: Project) -> dict[str, Any]:
        allocated = allocate_tasks(session, project.id)
        insight = self.analyze(
            "resource_allocation_agent_prompt.md",
            {
                "project_name": project.name,
                "allocated_count": len(allocated),
            },
        )
        return {"allocated_tasks": allocated, "allocation_insight": insight}
