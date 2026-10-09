from app.db.session import init_db
from app.db.session import engine
from app.core.auth import create_access_token
from sqlmodel import Session
import pytest


def auth_headers(role: str = "project_manager", subject: str = "1") -> dict[str, str]:
    token = create_access_token(subject=subject, role=role)
    return {"Authorization": f"Bearer {token}"}


def pytest_sessionstart(session):
    init_db()


@pytest.fixture
def session():
    with Session(engine) as db:
        yield db
