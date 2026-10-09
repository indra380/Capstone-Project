from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from app.api.deps import db_session
from app.core.auth import hash_password
from app.core.security import Role, require_permission, require_role
from app.models.entities import PermissionEntity, Project, ProjectMember, RoleEntity, UserAccount, UserRole
from app.schemas.api import (
    UserCreateRequest,
    UserProjectAssignRequest,
    UserRoleAssignRequest,
    UserUpdateRequest,
)
from app.schemas.domain import AdminSettingsIn, AdminSettingsOut
from app.services import admin, audit

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/settings", response_model=AdminSettingsOut)
def get_admin_settings(session: Session = Depends(db_session)):
    return admin.get_settings(session)


@router.put("/settings", response_model=AdminSettingsOut)
def update_admin_settings(
    payload: AdminSettingsIn,
    session: Session = Depends(db_session),
    role: Role = Depends(require_role({Role.ADMIN, Role.PROJECT_MANAGER})),
):
    updated = admin.upsert_settings(
        session,
        {
            "report_cadence": payload.report_cadence,
            "escalation_hours": payload.escalation_hours,
            "high_risk_threshold": payload.high_risk_threshold,
        },
    )
    audit.log_action(
        session,
        actor_role=role.value,
        action="admin_settings_updated",
        entity_type="settings",
        entity_id="global",
        rationale="Configuration updated by authorized role",
    )
    return updated


@router.get("/users")
def list_users(
    q: str = Query(default=""),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    is_active: bool | None = Query(default=None),
    session: Session = Depends(db_session),
    _: str = Depends(require_permission("users:manage")),
):
    statement = select(UserAccount)
    if q:
        like = f"%{q}%"
        statement = statement.where((UserAccount.full_name.like(like)) | (UserAccount.email.like(like)))
    if is_active is not None:
        statement = statement.where(UserAccount.is_active == is_active)
    rows = session.exec(statement.offset((page - 1) * page_size).limit(page_size)).all()
    return rows


@router.post("/users")
def create_user(
    payload: UserCreateRequest,
    session: Session = Depends(db_session),
    actor: Role = Depends(require_role({Role.SUPER_ADMIN, Role.ADMIN})),
):
    existing = session.exec(select(UserAccount).where(UserAccount.email == payload.email)).first()
    if existing:
        raise HTTPException(status_code=409, detail="Email already exists")

    role_name = Role.VIEWER.value
    if payload.role_ids:
        role_row = session.get(RoleEntity, payload.role_ids[0])
        if role_row:
            role_name = role_row.name

    user = UserAccount(
        full_name=payload.full_name,
        email=payload.email,
        password_hash=hash_password(payload.password),
        role=role_name,
        is_active=payload.is_active,
        skills_csv=",".join(payload.skill_list),
        password_changed_at=datetime.now(UTC),
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    for role_id in payload.role_ids:
        role_row = session.get(RoleEntity, role_id)
        if role_row:
            session.add(UserRole(user_id=user.id, role_id=role_id))
    session.commit()

    audit.log_action(
        session,
        actor_role=actor.value,
        action="admin_user_created",
        entity_type="user",
        entity_id=str(user.id),
        rationale="Admin created user",
    )
    return user


@router.patch("/users/{user_id}")
def update_user(
    user_id: int,
    payload: UserUpdateRequest,
    session: Session = Depends(db_session),
    actor: Role = Depends(require_role({Role.SUPER_ADMIN, Role.ADMIN})),
):
    user = session.get(UserAccount, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if payload.full_name is not None:
        user.full_name = payload.full_name
    if payload.is_active is not None:
        user.is_active = payload.is_active
    if payload.profile_picture_url is not None:
        user.profile_picture_url = payload.profile_picture_url
    if payload.skill_list is not None:
        user.skills_csv = ",".join(payload.skill_list)

    session.add(user)
    session.commit()

    audit.log_action(
        session,
        actor_role=actor.value,
        action="admin_user_updated",
        entity_type="user",
        entity_id=str(user.id),
        rationale="Admin updated user",
    )
    return user


@router.post("/users/{user_id}/roles")
def assign_user_roles(
    user_id: int,
    payload: UserRoleAssignRequest,
    session: Session = Depends(db_session),
    actor: Role = Depends(require_role({Role.SUPER_ADMIN, Role.ADMIN})),
):
    user = session.get(UserAccount, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    current = session.exec(select(UserRole).where(UserRole.user_id == user_id)).all()
    for row in current:
        session.delete(row)
    session.commit()

    role_name = Role.VIEWER.value
    for role_id in payload.role_ids:
        role_row = session.get(RoleEntity, role_id)
        if role_row:
            session.add(UserRole(user_id=user_id, role_id=role_id))
            role_name = role_row.name
    user.role = role_name
    session.add(user)
    session.commit()

    audit.log_action(
        session,
        actor_role=actor.value,
        action="admin_user_roles_assigned",
        entity_type="user",
        entity_id=str(user.id),
        rationale="Admin assigned user roles",
    )
    return {"ok": True}


@router.post("/users/{user_id}/projects")
def assign_user_projects(
    user_id: int,
    payload: UserProjectAssignRequest,
    session: Session = Depends(db_session),
    actor: Role = Depends(require_role({Role.SUPER_ADMIN, Role.ADMIN, Role.PROJECT_MANAGER})),
):
    user = session.get(UserAccount, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    existing = session.exec(select(ProjectMember).where(ProjectMember.user_id == user_id)).all()
    for row in existing:
        session.delete(row)
    session.commit()

    for project_id in payload.project_ids:
        project = session.get(Project, project_id)
        if project:
            session.add(ProjectMember(project_id=project_id, user_id=user_id, role=payload.role))
    session.commit()

    audit.log_action(
        session,
        actor_role=actor.value,
        action="admin_user_projects_assigned",
        entity_type="user",
        entity_id=str(user.id),
        rationale="User project assignments updated",
    )
    return {"ok": True}


@router.get("/roles")
def list_roles(
    session: Session = Depends(db_session),
    _: str = Depends(require_permission("users:manage")),
):
    return session.exec(select(RoleEntity)).all()


@router.get("/permissions")
def list_permissions(
    session: Session = Depends(db_session),
    _: str = Depends(require_permission("users:manage")),
):
    return session.exec(select(PermissionEntity)).all()
