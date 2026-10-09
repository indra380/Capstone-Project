from enum import Enum
from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select

from app.api.deps import db_session
from app.core.auth import get_current_identity
from app.models.entities import Project, ProjectMember, UserAccount


class Role(str, Enum):
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    PROJECT_MANAGER = "project_manager"
    TEAM_LEAD = "team_lead"
    TEAM_MEMBER = "team_member"
    STAKEHOLDER = "stakeholder"
    VIEWER = "viewer"


ROLE_PERMISSIONS: dict[Role, set[str]] = {
    Role.SUPER_ADMIN: {"*"},
    Role.ADMIN: {
        "users:manage",
        "projects:manage",
        "settings:manage",
        "analytics:view",
        "logs:view",
    },
    Role.PROJECT_MANAGER: {
        "projects:create",
        "projects:edit",
        "projects:delete_own",
        "members:assign",
        "ai:plan",
        "ai:allocate",
        "progress:manage",
        "risk:manage",
        "reports:generate",
        "dashboard:view",
    },
    Role.TEAM_LEAD: {
        "projects:view_assigned",
        "tasks:create",
        "tasks:assign",
        "tasks:update",
        "progress:view_team",
        "reports:generate_team",
        "team:communicate",
    },
    Role.TEAM_MEMBER: {
        "tasks:view_assigned",
        "tasks:update",
        "documents:upload",
        "comments:add",
        "timeline:view",
        "team:communicate",
    },
    Role.STAKEHOLDER: {
        "dashboard:view",
        "reports:view",
        "risks:view",
        "milestones:view",
        "progress:view",
    },
    Role.VIEWER: {
        "projects:view_assigned",
    },
}


def get_current_role(identity: dict = Depends(get_current_identity)) -> Role:
    x_role = str(identity.get("role", ""))
    try:
        return Role(x_role)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid role in token",
        ) from exc


def get_current_roles(identity: dict = Depends(get_current_identity)) -> set[Role]:
    raw = identity.get("roles") or [identity.get("role")]
    roles: set[Role] = set()
    for value in raw:
        if not value:
            continue
        try:
            roles.add(Role(str(value)))
        except ValueError:
            continue
    if not roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No valid role in token")
    return roles


def get_current_user(
    identity: dict = Depends(get_current_identity),
    session: Session = Depends(db_session),
) -> UserAccount:
    user_id = identity.get("sub")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token subject")
    user = session.get(UserAccount, int(user_id))
    if user is None or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is inactive or missing")
    return user


def require_role(allowed: set[Role]):
    def checker(parsed_roles: set[Role] = Depends(get_current_roles)) -> Role:
        common = parsed_roles.intersection(allowed)
        if not common:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions for this action",
            )
        # Return deterministic highest role in request context for audit compatibility.
        return sorted(common, key=lambda role: role.value)[0]

    return checker


def require_permission(permission: str):
    def checker(parsed_roles: set[Role] = Depends(get_current_roles)) -> str:
        for role in parsed_roles:
            grants = ROLE_PERMISSIONS.get(role, set())
            if "*" in grants or permission in grants:
                return permission
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Missing permission")

    return checker


def require_project_membership(write: bool = False):
    def checker(
        project_id: int,
        session: Session = Depends(db_session),
        user: UserAccount = Depends(get_current_user),
        parsed_roles: set[Role] = Depends(get_current_roles),
    ) -> int:
        if Role.SUPER_ADMIN in parsed_roles or Role.ADMIN in parsed_roles:
            return project_id

        project = session.get(Project, project_id)
        if project is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

        membership = session.exec(
            select(ProjectMember).where(
                ProjectMember.project_id == project_id,
                ProjectMember.user_id == user.id,
            )
        ).first()
        if membership is None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No project membership")

        if write and membership.role in {Role.STAKEHOLDER.value, Role.VIEWER.value}:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Read-only project role")

        return project_id

    return checker
