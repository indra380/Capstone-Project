# Project 15 - The AI Project Manager

Production-ready capstone implementation for AI-Forge 2026 Project 15.

## What This Delivers
- Supervisor-orchestrated workflow from goal intake to report generation.
- Feature modules for planning, allocation, progress, risk, communication, and admin settings.
- Role-aware API controls and manual override flow with audit trail.
- Dashboard UI for plan, progress, and risk visibility.
- Export support in JSON and CSV formats.
- CI pipeline with backend tests and frontend lint/build checks.

## Repository Structure
- `backend/` FastAPI service and orchestration logic.
- `frontend/` Next.js dashboard and intake UI.
- `.github/workflows/` CI workflow.
- `docker-compose.yml` local multi-service runtime.

## Quick Start (Local)
### 1) Backend
```powershell
cd backend
python -m venv ..\.venv
..\.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 2) Frontend
```powershell
cd frontend
npm install
npm run dev
```

- Frontend URL: http://localhost:3000
- Backend URL: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Docker Run
```powershell
docker compose up --build
```

## Core API Endpoints
- `POST /api/v1/projects` Goal intake and full orchestration kickoff.
- `GET /api/v1/projects/{id}/overview` Dashboard summary.
- `PATCH /api/v1/projects/{id}/tasks/{taskId}` Progress update.
- `POST /api/v1/projects/{id}/override` Manual assignment override with rationale.
- `GET /api/v1/projects/{id}/export?format=json|csv` Governance export.
- `GET /api/v1/admin/settings` and `PUT /api/v1/admin/settings` Admin controls.

## Default Demo Flow
1. Open home page and submit goal intake.
2. Review generated plan and risks in dashboard.
3. Update task statuses and re-check risks.
4. Trigger report generation and review report history.
5. Execute manual override and inspect audit log records via DB.

## Notes
- This scaffold uses SQLite for local speed and easy demo reliability.
- Production deployment should switch to managed PostgreSQL and managed Redis.
