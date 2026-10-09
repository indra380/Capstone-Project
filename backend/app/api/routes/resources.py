from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.api.deps import db_session
from app.core.security import Role, require_role
from app.models.entities import Resource
from app.schemas.api import ResourceCreateRequest, ResourceUpdateRequest

router = APIRouter(prefix="/resources", tags=["resources"])


@router.post("", status_code=201)
def create_resource(
    payload: ResourceCreateRequest,
    session: Session = Depends(db_session),
    role: Role = Depends(require_role({Role.ADMIN, Role.PROJECT_MANAGER, Role.TEAM_LEAD})),
):
    resource = Resource(
        name=payload.name,
        role=payload.role,
        skills_csv=payload.skills_csv,
        availability_percent=payload.availability_percent,
    )
    session.add(resource)
    session.commit()
    session.refresh(resource)
    return resource


@router.get("")
def list_resources(
    session: Session = Depends(db_session),
    role: Role = Depends(require_role({Role.ADMIN, Role.PROJECT_MANAGER, Role.TEAM_LEAD, Role.TEAM_MEMBER, Role.STAKEHOLDER})),
):
    return session.exec(select(Resource)).all()


@router.get("/{resource_id}")
def get_resource(
    resource_id: int,
    session: Session = Depends(db_session),
    role: Role = Depends(require_role({Role.ADMIN, Role.PROJECT_MANAGER, Role.TEAM_LEAD, Role.TEAM_MEMBER, Role.STAKEHOLDER})),
):
    resource = session.get(Resource, resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resource


@router.put("/{resource_id}")
def update_resource(
    resource_id: int,
    payload: ResourceUpdateRequest,
    session: Session = Depends(db_session),
    role: Role = Depends(require_role({Role.ADMIN, Role.PROJECT_MANAGER, Role.TEAM_LEAD})),
):
    resource = session.get(Resource, resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(resource, key, value)

    session.add(resource)
    session.commit()
    session.refresh(resource)
    return resource


@router.delete("/{resource_id}", status_code=204)
def delete_resource(
    resource_id: int,
    session: Session = Depends(db_session),
    role: Role = Depends(require_role({Role.ADMIN, Role.PROJECT_MANAGER})),
):
    resource = session.get(Resource, resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    session.delete(resource)
    session.commit()
    return None
