from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from app.models.entities import TaskStatus, RiskSeverity


class CreateProjectRequest(BaseModel):
    name: str = Field(min_length=3, max_length=120)
    goal: str = Field(min_length=8, max_length=2000)
    deadline: Optional[datetime] = None


class ResourceIn(BaseModel):
    name: str
    role: str
    skills: list[str]
    availability_percent: int = Field(default=100, ge=0, le=100)


class TaskOut(BaseModel):
    id: int
    title: str
    description: str
    owner_id: Optional[int]
    status: TaskStatus
    duration_days: int
    milestone: str
    depends_on: list[int]


class RiskOut(BaseModel):
    id: int
    title: str
    severity: RiskSeverity
    mitigation: str


class StatusUpdateRequest(BaseModel):
    status: TaskStatus
    reason: Optional[str] = ""


class OverrideRequest(BaseModel):
    task_id: int
    owner_id: int
    rationale: str = Field(min_length=5, max_length=500)


class ProjectSnapshotOut(BaseModel):
    project_id: int
    project_name: str
    completion_percent: int
    blocked_tasks: int
    high_risks: int
    report_cadence: str
    ai_summary: str = ""
    ai_recommendations: list[str] = []


class AdminSettingsIn(BaseModel):
    report_cadence: str = Field(default="daily", pattern="^(daily|weekly)$")
    escalation_hours: int = Field(default=4, ge=1, le=72)
    high_risk_threshold: int = Field(default=2, ge=1, le=10)


class AdminSettingsOut(BaseModel):
    report_cadence: str
    escalation_hours: int
    high_risk_threshold: int
