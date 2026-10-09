import sys
from sqlmodel import Session, SQLModel, create_engine, select

from app.core.auth import hash_password
from app.core.config import get_settings
from app.models.entities import PermissionEntity, RoleEntity, UserAccount, UserRole


ROLE_PERMISSIONS_SEED: dict[str, set[str]] = {
    "super_admin": {"*"},
    "admin": {"users:manage", "projects:manage", "settings:manage", "analytics:view", "logs:view"},
    "project_manager": {
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
    "team_lead": {
        "projects:view_assigned",
        "tasks:create",
        "tasks:assign",
        "tasks:update",
        "progress:view_team",
        "reports:generate_team",
        "team:communicate",
    },
    "team_member": {
        "tasks:view_assigned",
        "tasks:update",
        "documents:upload",
        "comments:add",
        "timeline:view",
        "team:communicate",
    },
    "stakeholder": {"dashboard:view", "reports:view", "risks:view", "milestones:view", "progress:view"},
    "viewer": {"projects:view_assigned"},
}


settings = get_settings()
database_url = settings.database_url

# Keep tests self-contained and independent from external DB drivers/services.
if "pytest" in sys.modules:
    database_url = "sqlite:///./project15_test.db"

connect_args = {"check_same_thread": False} if database_url.startswith("sqlite") else {}
engine = create_engine(database_url, echo=False, connect_args=connect_args)


def init_db() -> None:
    from app.models import entities  # noqa: F401

    SQLModel.metadata.create_all(engine)

    if "pytest" in sys.modules:
        return

    with Session(engine) as session:
        _seed_roles_permissions(session)
        _seed_demo_users(session)


def _seed_roles_permissions(session: Session) -> None:
    role_name_to_id: dict[str, int] = {}
    for role_name in ROLE_PERMISSIONS_SEED:
        row = session.exec(select(RoleEntity).where(RoleEntity.name == role_name)).first()
        if row is None:
            row = RoleEntity(name=role_name, description=f"System role: {role_name}")
            session.add(row)
            session.commit()
            session.refresh(row)
        role_name_to_id[role_name] = row.id

    for grants in ROLE_PERMISSIONS_SEED.values():
        for permission in grants:
            if permission == "*":
                continue
            existing = session.exec(select(PermissionEntity).where(PermissionEntity.code == permission)).first()
            if existing is None:
                session.add(
                    PermissionEntity(
                        code=permission,
                        name=permission.replace(":", " ").replace("_", " ").title(),
                        description="Seeded system permission",
                    )
                )
    session.commit()


def _seed_demo_users(session: Session) -> None:
    demo_users = [
        ("admin@aipm.local", "Admin User", "Admin@123", "admin"),
        ("manager@aipm.local", "Project Manager", "Manager@123", "project_manager"),
        ("lead@aipm.local", "Team Lead", "Lead@123", "team_lead"),
        ("member@aipm.local", "Team Member", "Member@123", "team_member"),
        ("stakeholder@aipm.local", "Stakeholder", "Stakeholder@123", "stakeholder"),
        ("viewer@aipm.local", "Viewer", "Viewer@123", "viewer"),
    ]

    for email, full_name, raw_password, role_name in demo_users:
        user = session.exec(select(UserAccount).where(UserAccount.email == email)).first()
        if user is None:
            user = UserAccount(
                full_name=full_name,
                email=email,
                password_hash=hash_password(raw_password),
                role=role_name,
                email_verified=True,
                is_active=True,
            )
            session.add(user)
            session.commit()
            session.refresh(user)

        role_row = session.exec(select(RoleEntity).where(RoleEntity.name == role_name)).first()
        if role_row is None:
            continue
        existing_link = session.exec(
            select(UserRole).where(UserRole.user_id == user.id, UserRole.role_id == role_row.id)
        ).first()
        if existing_link is None:
            session.add(UserRole(user_id=user.id, role_id=role_row.id))
            session.commit()


def get_session():
    with Session(engine) as session:
        yield session
