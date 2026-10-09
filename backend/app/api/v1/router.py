from fastapi import APIRouter

from app.api.routes.admin import router as admin_router
from app.api.routes.ai_actions import router as ai_actions_router
from app.api.routes.auth import router as auth_router
from app.api.routes.dashboard import router as dashboard_router
from app.api.routes.health import router as health_router
from app.api.routes.projects import router as projects_router
from app.api.routes.reports import router as reports_router
from app.api.routes.resources import router as resources_router
from app.api.routes.risks import router as risks_router
from app.api.routes.tasks import router as tasks_router

api_v1_router = APIRouter()
api_v1_router.include_router(health_router)
api_v1_router.include_router(auth_router)
api_v1_router.include_router(projects_router)
api_v1_router.include_router(tasks_router)
api_v1_router.include_router(resources_router)
api_v1_router.include_router(risks_router)
api_v1_router.include_router(reports_router)
api_v1_router.include_router(dashboard_router)
api_v1_router.include_router(ai_actions_router)
api_v1_router.include_router(admin_router)
