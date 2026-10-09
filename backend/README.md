# Backend Service

FastAPI service for Project 15 orchestration and core feature APIs.

## Architecture (Phase 2)
- `app/main.py`: process entrypoint, delegates to app factory.
- `app/core/app_factory.py`: app creation, middleware, lifecycle, router registration.
- `app/core/logging.py`: centralized Loguru setup and stdlib interception.
- `app/core/exceptions.py`: global exception handlers and uniform error payloads.
- `app/api/v1/router.py`: versioned route composition.
- `app/repositories/`: repository layer package (data access abstractions).
- `app/use_cases/`: use-case layer package (application workflows).
- `app/common/`: shared contracts/utilities.

## Database (Phase 3)
- PostgreSQL is configured through `DATABASE_URL` in `.env`.
- Supabase Postgres URLs are supported directly.
- SQLAlchemy production schema is defined in `app/db/sqlalchemy/models.py`.
- Alembic migration environment is configured under `alembic/`.

### Apply Migrations
```powershell
pip install -r requirements.txt
alembic upgrade head
```

### Create New Migration
```powershell
alembic revision --autogenerate -m "describe change"
alembic upgrade head
```

## LangGraph Workflow (Phase 4)
- Workflow module: `app/workflows/project_workflow.py`
- State graph sequence:
	- Supervisor -> Planning -> Resource Allocation -> Progress Tracking -> Risk Assessment -> Communication -> END
- Supervisor service delegates orchestration to LangGraph workflow execution.

## AI Agents (Phase 5)
- Agent implementations:
	- `app/agents/supervisor_agent.py`
	- `app/agents/planning_agent.py`
	- `app/agents/resource_allocation_agent.py`
	- `app/agents/progress_tracking_agent.py`
	- `app/agents/risk_assessment_agent.py`
	- `app/agents/communication_agent.py`
- Shared agent base: `app/agents/base.py`
- Prompt templates: `../prompts/*.md`
- Configurable LLM provider support:
	- OpenAI (default)
	- Gemini (via `AI_PROVIDER=gemini` and Gemini API settings)

## REST API (Phase 6)
- Authentication:
	- `POST /api/v1/auth/register`
	- `POST /api/v1/auth/login`
- Projects:
	- `GET /api/v1/projects`
	- `POST /api/v1/projects`
	- `GET /api/v1/projects/{project_id}`
	- `PUT /api/v1/projects/{project_id}`
	- `DELETE /api/v1/projects/{project_id}`
- Tasks CRUD:
	- `POST /api/v1/tasks`
	- `GET /api/v1/tasks`
	- `GET /api/v1/tasks/{task_id}`
	- `PUT /api/v1/tasks/{task_id}`
	- `DELETE /api/v1/tasks/{task_id}`
- Resources CRUD:
	- `POST /api/v1/resources`
	- `GET /api/v1/resources`
	- `GET /api/v1/resources/{resource_id}`
	- `PUT /api/v1/resources/{resource_id}`
	- `DELETE /api/v1/resources/{resource_id}`
- Risks CRUD:
	- `POST /api/v1/risks`
	- `GET /api/v1/risks`
	- `GET /api/v1/risks/{risk_id}`
	- `PUT /api/v1/risks/{risk_id}`
	- `DELETE /api/v1/risks/{risk_id}`
- Reports:
	- `GET /api/v1/reports`
	- `GET /api/v1/reports/{report_id}`
	- `POST /api/v1/reports/generate`
- Dashboard:
	- `GET /api/v1/dashboard/analytics?project_id=...`
- AI Actions:
	- `POST /api/v1/ai/generate-project-plan`
	- `POST /api/v1/ai/allocate-resources`
	- `POST /api/v1/ai/risk-assessment`
	- `POST /api/v1/ai/generate-status-report`
	- `POST /api/v1/ai/run-supervisor`

## Run
```powershell
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Tests
```powershell
pytest -q
```
