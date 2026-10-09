from datetime import UTC, datetime
from enum import Enum
from typing import Optional
from sqlmodel import SQLModel, Field


class AccountStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class TaskStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    DONE = "done"


class RiskSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class UserAccount(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str
    email: str = Field(index=True, unique=True)
    password_hash: str
    role: str = "viewer"
    is_active: bool = True
    status: AccountStatus = AccountStatus.ACTIVE
    email_verified: bool = False
    profile_picture_url: str = ""
    skills_csv: str = ""
    failed_login_attempts: int = 0
    locked_until: Optional[datetime] = None
    password_changed_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class RoleEntity(SQLModel, table=True):
    __tablename__ = "roles"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    description: str = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class PermissionEntity(SQLModel, table=True):
    __tablename__ = "permissions"

    id: Optional[int] = Field(default=None, primary_key=True)
    code: str = Field(index=True, unique=True)
    name: str
    description: str = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class RolePermission(SQLModel, table=True):
    __tablename__ = "role_permissions"

    id: Optional[int] = Field(default=None, primary_key=True)
    role_id: int = Field(index=True)
    permission_id: int = Field(index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class UserRole(SQLModel, table=True):
    __tablename__ = "user_roles"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    role_id: int = Field(index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class Project(SQLModel, table=True):
    __tablename__ = "projects"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    goal: str
    owner_id: Optional[int] = Field(default=None, index=True)
    deadline: Optional[datetime] = None
    status: str = "active"
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class ProjectMember(SQLModel, table=True):
    __tablename__ = "project_members"

    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(index=True)
    user_id: int = Field(index=True)
    role: str = Field(default="viewer")
    joined_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class Resource(SQLModel, table=True):
    __tablename__ = "resources"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    role: str
    skills_csv: str
    availability_percent: int = 100


class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(index=True)
    title: str
    description: str = ""
    owner_id: Optional[int] = Field(default=None, index=True)
    status: TaskStatus = TaskStatus.NOT_STARTED
    duration_days: int = 1
    milestone: str = ""
    depends_on_csv: str = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class Risk(SQLModel, table=True):
    __tablename__ = "risks"

    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(index=True)
    title: str
    severity: RiskSeverity
    mitigation: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class Report(SQLModel, table=True):
    __tablename__ = "reports"

    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(index=True)
    cadence: str = "daily"
    content: str
    snapshot_json: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class AuditLog(SQLModel, table=True):
    __tablename__ = "audit_logs"

    id: Optional[int] = Field(default=None, primary_key=True)
    actor_role: str
    actor_user_id: Optional[int] = Field(default=None, index=True)
    ip_address: str = ""
    action: str
    entity_type: str
    entity_id: str
    rationale: str = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class SystemSetting(SQLModel, table=True):
    __tablename__ = "system_settings"

    id: Optional[int] = Field(default=None, primary_key=True)
    key: str = Field(index=True, unique=True)
    value: str
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class SessionEntity(SQLModel, table=True):
    __tablename__ = "sessions"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    session_key: str = Field(index=True, unique=True)
    ip_address: str = ""
    user_agent: str = ""
    is_active: bool = True
    last_seen_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    expires_at: datetime
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class RefreshTokenEntity(SQLModel, table=True):
    __tablename__ = "refresh_tokens"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    session_id: int = Field(index=True)
    token_hash: str = Field(index=True, unique=True)
    expires_at: datetime
    revoked_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class PasswordResetToken(SQLModel, table=True):
    __tablename__ = "password_reset_tokens"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    token_hash: str = Field(index=True, unique=True)
    expires_at: datetime
    used_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class EmailVerificationToken(SQLModel, table=True):
    __tablename__ = "email_verification_tokens"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    token_hash: str = Field(index=True, unique=True)
    expires_at: datetime
    used_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
