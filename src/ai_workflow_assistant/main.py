from fastapi import FastAPI

from ai_workflow_assistant.api.routes.health import router as health_router
from ai_workflow_assistant.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

app.include_router(health_router)
