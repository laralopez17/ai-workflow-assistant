from pydantic import BaseModel, field_validator

from ai_workflow_assistant.domain.models import WorkflowRun


class WorkflowRunRequest(BaseModel):
    content: str

    @field_validator("content")
    @classmethod
    def content_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("content must not be empty or whitespace-only")
        return value


class WorkflowRunResponse(BaseModel):
    run: WorkflowRun
