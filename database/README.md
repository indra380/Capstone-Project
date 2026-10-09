# Database Layer (Phase 3)

This project now includes a production-grade PostgreSQL database architecture using SQLAlchemy and Alembic.

## Stack
- PostgreSQL (Supabase-compatible)
- SQLAlchemy 2.x
- Alembic migrations

## Location
- SQLAlchemy models: `backend/app/db/sqlalchemy/models.py`
- Session/engine: `backend/app/db/sqlalchemy/session.py`
- Alembic config: `backend/alembic.ini`
- Alembic env: `backend/alembic/env.py`
- Initial migration: `backend/alembic/versions/20260629_0001_initial_schema.py`

## Entities Implemented
- Users
- Projects
- Tasks
- Assignments
- Milestones
- Skills
- Resources
- Risks
- Reports
- Meetings
- ActivityLogs
- Embeddings

## Run Migrations
```powershell
cd backend
pip install -r requirements.txt
alembic upgrade head
```
