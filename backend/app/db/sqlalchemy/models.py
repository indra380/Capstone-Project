from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum

from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    Enum as SAEnum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.sqlalchemy.base import Base


class Role(str, Enum):
    ADMIN = "admin"
    PROJECT_MANAGER = "project_manager"
    TEAM_LEAD = "team_lead"
    TEAM_MEMBER = "team_member"
    STAKEHOLDER = "stakeholder"


class TaskStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    DONE = "done"


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ReportType(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    STAKEHOLDER = "stakeholder"
    MEETING = "meeting"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[Role] = mapped_column(SAEnum(Role, name="role_enum"), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC), nullable=False)

    owned_projects: Mapped[list[Project]] = relationship("Project", back_populates="owner")
    activity_logs: Mapped[list[ActivityLog]] = relationship("ActivityLog", back_populates="actor")


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    goal: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(40), default="active", nullable=False)
    start_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    deadline: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    owner_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC), nullable=False)

    owner: Mapped[User | None] = relationship("User", back_populates="owned_projects")
    tasks: Mapped[list[Task]] = relationship("Task", back_populates="project", cascade="all, delete-orphan")
    milestones: Mapped[list[Milestone]] = relationship(
        "Milestone", back_populates="project", cascade="all, delete-orphan"
    )
    risks: Mapped[list[Risk]] = relationship("Risk", back_populates="project", cascade="all, delete-orphan")
    reports: Mapped[list[Report]] = relationship("Report", back_populates="project", cascade="all, delete-orphan")
    meetings: Mapped[list[Meeting]] = relationship(
        "Meeting", back_populates="project", cascade="all, delete-orphan"
    )
    embeddings: Mapped[list[Embedding]] = relationship(
        "Embedding", back_populates="project", cascade="all, delete-orphan"
    )


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[TaskStatus] = mapped_column(
        SAEnum(TaskStatus, name="task_status_enum"),
        default=TaskStatus.NOT_STARTED,
        nullable=False,
    )
    priority: Mapped[str] = mapped_column(String(20), default="medium", nullable=False)
    estimated_hours: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    due_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC), nullable=False)

    project: Mapped[Project] = relationship("Project", back_populates="tasks")
    assignments: Mapped[list[Assignment]] = relationship(
        "Assignment", back_populates="task", cascade="all, delete-orphan"
    )


class Resource(Base):
    __tablename__ = "resources"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    role: Mapped[str] = mapped_column(String(100), nullable=False)
    experience_years: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    availability_percent: Mapped[int] = mapped_column(Integer, default=100, nullable=False)
    workload_percent: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC), nullable=False)

    assignments: Mapped[list[Assignment]] = relationship(
        "Assignment", back_populates="resource", cascade="all, delete-orphan"
    )
    skills: Mapped[list[Skill]] = relationship(
        "Skill", secondary="resource_skills", back_populates="resources"
    )


class Skill(Base):
    __tablename__ = "skills"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    category: Mapped[str | None] = mapped_column(String(120), nullable=True)

    resources: Mapped[list[Resource]] = relationship(
        "Resource", secondary="resource_skills", back_populates="skills"
    )


class ResourceSkill(Base):
    __tablename__ = "resource_skills"
    __table_args__ = (UniqueConstraint("resource_id", "skill_id", name="uq_resource_skill"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    resource_id: Mapped[int] = mapped_column(ForeignKey("resources.id", ondelete="CASCADE"), index=True)
    skill_id: Mapped[int] = mapped_column(ForeignKey("skills.id", ondelete="CASCADE"), index=True)
    proficiency: Mapped[int] = mapped_column(Integer, default=3, nullable=False)


class Assignment(Base):
    __tablename__ = "assignments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"), index=True)
    resource_id: Mapped[int] = mapped_column(ForeignKey("resources.id", ondelete="CASCADE"), index=True)
    allocation_percent: Mapped[int] = mapped_column(Integer, default=100, nullable=False)
    assigned_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC), nullable=False)

    task: Mapped[Task] = relationship("Task", back_populates="assignments")
    resource: Mapped[Resource] = relationship("Resource", back_populates="assignments")


class Milestone(Base):
    __tablename__ = "milestones"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    due_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String(40), default="planned", nullable=False)

    project: Mapped[Project] = relationship("Project", back_populates="milestones")


class Risk(Base):
    __tablename__ = "risks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), index=True)
    task_id: Mapped[int | None] = mapped_column(ForeignKey("tasks.id", ondelete="SET NULL"), nullable=True)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    probability: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    impact: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    level: Mapped[RiskLevel] = mapped_column(SAEnum(RiskLevel, name="risk_level_enum"), nullable=False)
    mitigation: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(40), default="open", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC), nullable=False)

    project: Mapped[Project] = relationship("Project", back_populates="risks")


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), index=True)
    generated_by_user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    report_type: Mapped[ReportType] = mapped_column(
        SAEnum(ReportType, name="report_type_enum"),
        nullable=False,
    )
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    metadata_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC), nullable=False)

    project: Mapped[Project] = relationship("Project", back_populates="reports")


class Meeting(Base):
    __tablename__ = "meetings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    agenda: Mapped[str | None] = mapped_column(Text, nullable=True)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    attendees_json: Mapped[list | None] = mapped_column(JSON, nullable=True)
    action_items_json: Mapped[list | None] = mapped_column(JSON, nullable=True)
    meeting_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC), nullable=False)

    project: Mapped[Project] = relationship("Project", back_populates="meetings")


class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    project_id: Mapped[int | None] = mapped_column(ForeignKey("projects.id", ondelete="SET NULL"), nullable=True)
    actor_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    action: Mapped[str] = mapped_column(String(150), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(80), nullable=False)
    entity_id: Mapped[str] = mapped_column(String(80), nullable=False)
    details_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC), nullable=False)

    actor: Mapped[User | None] = relationship("User", back_populates="activity_logs")


class Embedding(Base):
    __tablename__ = "embeddings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), index=True)
    source_type: Mapped[str] = mapped_column(String(50), nullable=False)
    source_id: Mapped[str] = mapped_column(String(120), nullable=False)
    chunk_text: Mapped[str] = mapped_column(Text, nullable=False)
    faiss_id: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    embedding_meta_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC), nullable=False)

    project: Mapped[Project] = relationship("Project", back_populates="embeddings")
