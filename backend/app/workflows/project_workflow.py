from __future__ import annotations

from typing import Any, TypedDict

from langgraph.graph import END, START, StateGraph
from loguru import logger
from sqlmodel import Session

from app.agents import (
    CommunicationAgent,
    PlanningAgent,
    ProgressTrackingAgent,
    ResourceAllocationAgent,
    RiskAssessmentAgent,
    SupervisorAgent,
)
from app.models.entities import Project


class WorkflowState(TypedDict, total=False):
    session: Session
    project: Project
    cadence: str
    ai_summary: str
    ai_risks: list[str]
    ai_recommendations: list[str]
    plan_tasks: list[Any]
    planning_insight: dict[str, Any]
    allocated_tasks: list[Any]
    allocation_insight: dict[str, Any]
    progress_snapshot: dict[str, Any]
    progress_insight: dict[str, Any]
    risk_entries: list[Any]
    risk_insight: dict[str, Any]
    report: Any
    communication_insight: dict[str, Any]
    step_errors: list[dict[str, Any]]


def _supervisor_node(state: WorkflowState) -> WorkflowState:
    def _run(current: WorkflowState) -> WorkflowState:
        project = current["project"]
        cadence = current.get("cadence", "daily")
        agent = SupervisorAgent()
        return agent.run(project.goal, cadence)

    fallback = {
        "ai_summary": "Supervisor fallback engaged: downstream execution continues with defaults.",
        "ai_risks": ["supervisor_unavailable"],
        "ai_recommendations": ["Review orchestration logs and rerun the workflow."],
    }
    return _run_with_retry("supervisor", state, _run, fallback)


def _planning_node(state: WorkflowState) -> WorkflowState:
    def _run(current: WorkflowState) -> WorkflowState:
        session = current["session"]
        project = current["project"]
        agent = PlanningAgent()
        return agent.run(session, project)

    return _run_with_retry("planning", state, _run, {"plan_tasks": [], "planning_insight": {"fallback": True}})


def _allocation_node(state: WorkflowState) -> WorkflowState:
    def _run(current: WorkflowState) -> WorkflowState:
        session = current["session"]
        project = current["project"]
        agent = ResourceAllocationAgent()
        return agent.run(session, project)

    return _run_with_retry("allocation", state, _run, {"allocated_tasks": [], "allocation_insight": {"fallback": True}})


def _progress_node(state: WorkflowState) -> WorkflowState:
    def _run(current: WorkflowState) -> WorkflowState:
        session = current["session"]
        project = current["project"]
        agent = ProgressTrackingAgent()
        return agent.run(session, project)

    fallback = {
        "progress_snapshot": {"completion_percent": 0, "blocked_tasks": 0, "total": 0},
        "progress_insight": {"fallback": True},
    }
    return _run_with_retry("progress", state, _run, fallback)


def _risk_node(state: WorkflowState) -> WorkflowState:
    def _run(current: WorkflowState) -> WorkflowState:
        session = current["session"]
        project = current["project"]
        agent = RiskAssessmentAgent()
        return agent.run(session, project)

    return _run_with_retry("risk", state, _run, {"risk_entries": [], "risk_insight": {"fallback": True}})


def _communication_node(state: WorkflowState) -> WorkflowState:
    def _run(current: WorkflowState) -> WorkflowState:
        session = current["session"]
        project = current["project"]
        cadence = current.get("cadence", "daily")
        agent = CommunicationAgent()
        return agent.run(session, project, cadence)

    return _run_with_retry("communication", state, _run, {"report": None, "communication_insight": {"fallback": True}})


def _run_with_retry(
    step: str,
    state: WorkflowState,
    handler,
    fallback: dict[str, Any],
    max_attempts: int = 2,
) -> WorkflowState:
    errors = list(state.get("step_errors", []))
    last_error: Exception | None = None

    for attempt in range(1, max_attempts + 1):
        try:
            result = handler(state)
            result["step_errors"] = errors
            return result
        except Exception as exc:
            last_error = exc
            logger.warning("Workflow step {} failed on attempt {}: {}", step, attempt, exc)

    errors.append(
        {
            "step": step,
            "error": str(last_error) if last_error else "unknown",
            "attempts": max_attempts,
            "fallback": True,
        }
    )

    outcome = dict(fallback)
    outcome["step_errors"] = errors
    return outcome


def build_project_workflow():
    graph = StateGraph(WorkflowState)
    graph.add_node("supervisor", _supervisor_node)
    graph.add_node("planning", _planning_node)
    graph.add_node("allocation", _allocation_node)
    graph.add_node("progress", _progress_node)
    graph.add_node("risk", _risk_node)
    graph.add_node("communication", _communication_node)

    graph.add_edge(START, "supervisor")
    graph.add_edge("supervisor", "planning")
    graph.add_edge("planning", "allocation")
    graph.add_edge("allocation", "progress")
    graph.add_edge("progress", "risk")
    graph.add_edge("risk", "communication")
    graph.add_edge("communication", END)

    return graph.compile()


_WORKFLOW = build_project_workflow()


def run_project_workflow(session: Session, project: Project, cadence: str = "daily") -> dict[str, Any]:
    state: WorkflowState = {
        "session": session,
        "project": project,
        "cadence": cadence,
    }
    try:
        result = _WORKFLOW.invoke(state)
    except Exception as exc:
        logger.exception("Workflow execution failed")
        return {
            "task_count": 0,
            "risk_count": 0,
            "completion_percent": 0,
            "report_id": None,
            "ai_summary": "Workflow execution failed before completion.",
            "ai_recommendations": ["Check workflow logs and retry orchestration."],
            "status": "failed",
            "errors": [{"step": "workflow", "error": str(exc), "fallback": False}],
        }

    step_errors = result.get("step_errors", [])
    status = "degraded" if step_errors else "ok"
    return {
        "task_count": len(result.get("plan_tasks", [])),
        "risk_count": len(result.get("risk_entries", [])),
        "completion_percent": result.get("progress_snapshot", {}).get("completion_percent", 0),
        "report_id": getattr(result.get("report"), "id", None),
        "ai_summary": result.get("ai_summary", ""),
        "ai_recommendations": result.get("ai_recommendations", []),
        "status": status,
        "errors": step_errors,
    }
