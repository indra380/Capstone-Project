from __future__ import annotations

from typing import Any

from app.agents.base import BaseAgent


class SupervisorAgent(BaseAgent):
    name = "supervisor"

    def run(self, project_goal: str, cadence: str) -> dict[str, Any]:
        insight = self.analyze(
            "supervisor_agent_prompt.md",
            {"goal": project_goal, "cadence": cadence},
        )
        return {
            "ai_summary": insight.get("summary", ""),
            "ai_risks": insight.get("risks", []),
            "ai_recommendations": insight.get("recommendations", []),
        }
