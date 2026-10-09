from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, EmailStr


class RegisterRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=150)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    role: str = Field(default="team_member")


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class AuthResponse(TokenOut):
    refresh_token: str
    session_id: str
    roles: list[str] = []


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(min_length=8, max_length=128)


class ChangePasswordRequest(BaseModel):
    current_password: str = Field(min_length=8, max_length=128)
    new_password: str = Field(min_length=8, max_length=128)


class SessionOut(BaseModel):
    session_id: str
    ip_address: str
    user_agent: str
    is_active: bool
    last_seen_at: datetime
    expires_at: datetime


class ProjectUpdateRequest(BaseModel):
    name: Optional[str] = Field(default=None, min_length=3, max_length=120)
    goal: Optional[str] = Field(default=None, min_length=8, max_length=2000)
    deadline: Optional[datetime] = None
    status: Optional[str] = None


class TaskCreateRequest(BaseModel):
    project_id: int
    title: str = Field(min_length=3, max_length=200)
    description: str = ""
    duration_days: int = Field(default=1, ge=1, le=365)
    milestone: str = ""


class TaskUpdateRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    duration_days: Optional[int] = Field(default=None, ge=1, le=365)
    milestone: Optional[str] = None
    owner_id: Optional[int] = None


class ResourceCreateRequest(BaseModel):
    name: str
    role: str
    skills_csv: str
    availability_percent: int = Field(default=100, ge=0, le=100)


class ResourceUpdateRequest(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    skills_csv: Optional[str] = None
    availability_percent: Optional[int] = Field(default=None, ge=0, le=100)


class RiskCreateRequest(BaseModel):
    project_id: int
    title: str
    severity: str = Field(pattern="^(low|medium|high|critical)$")
    mitigation: str


class RiskUpdateRequest(BaseModel):
    title: Optional[str] = None
    severity: Optional[str] = Field(default=None, pattern="^(low|medium|high|critical)$")
    mitigation: Optional[str] = None


class GenerateReportRequest(BaseModel):
    project_id: int
    cadence: str = Field(default="daily", pattern="^(daily|weekly)$")
    channel: str = Field(default="email")


class AIProjectRequest(BaseModel):
    project_id: int


class AIStatusReportRequest(BaseModel):
    project_id: int
    cadence: str = Field(default="daily", pattern="^(daily|weekly)$")


class UserCreateRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=150)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    is_active: bool = True
    role_ids: list[int] = []
    skill_list: list[str] = []


class UserUpdateRequest(BaseModel):
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
    profile_picture_url: Optional[str] = None
    skill_list: Optional[list[str]] = None


class UserRoleAssignRequest(BaseModel):
    role_ids: list[int]


class UserProjectAssignRequest(BaseModel):
    project_ids: list[int]
    role: str = "team_member"
