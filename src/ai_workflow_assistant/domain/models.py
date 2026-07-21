from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

from ai_workflow_assistant.domain.enums import (
    Priority,
    StepStatus,
    TaskStatus,
    WorkflowStatus,
)


class ProjectNote(BaseModel):
    content: str

    @field_validator("content")
    @classmethod
    def content_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("content must not be empty or whitespace-only")
        return value


class ActionItem(BaseModel):
    description: str
    priority: Priority = Priority.medium
    status: TaskStatus = TaskStatus.todo
    owner: str | None = None
    due_date: str | None = None
    source_text: str | None = None
    tags: list[str] = Field(default_factory=list)
    missing_info: list[str] = Field(default_factory=list)
    confidence: float | None = None

    @field_validator("description")
    @classmethod
    def description_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("description must not be empty")
        return value

    @field_validator("confidence")
    @classmethod
    def confidence_must_be_in_range(cls, value: float | None) -> float | None:
        if value is not None and not 0.0 <= value <= 1.0:
            raise ValueError("confidence must be between 0 and 1")
        return value


class Blocker(BaseModel):
    description: str
    severity: Priority = Priority.medium
    source_text: str | None = None
    suggested_resolution: str | None = None
    missing_info: list[str] = Field(default_factory=list)
    confidence: float | None = None

    @field_validator("description")
    @classmethod
    def description_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("description must not be empty")
        return value

    @field_validator("confidence")
    @classmethod
    def confidence_must_be_in_range(cls, value: float | None) -> float | None:
        if value is not None and not 0.0 <= value <= 1.0:
            raise ValueError("confidence must be between 0 and 1")
        return value


class ChecklistItem(BaseModel):
    description: str
    is_completed: bool = False
    source_action_item_index: int | None = None

    @field_validator("description")
    @classmethod
    def description_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("description must not be empty")
        return value


class ExecutionPlan(BaseModel):
    objective: str
    steps: list[str] = Field(default_factory=list)
    priority: Priority = Priority.medium

    @field_validator("objective")
    @classmethod
    def objective_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("objective must not be empty")
        return value

    @field_validator("steps")
    @classmethod
    def steps_must_not_contain_empty_strings(cls, value: list[str]) -> list[str]:
        if any(not step.strip() for step in value):
            raise ValueError("steps must not contain empty strings")
        return value


class WorkflowStep(BaseModel):
    name: str
    status: StepStatus = StepStatus.pending
    tool_name: str | None = None
    summary: str | None = None
    error: str | None = None

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("name must not be empty")
        return value


class FinalReport(BaseModel):
    summary: str
    overall_priority: Priority = Priority.medium
    action_items: list[ActionItem] = Field(default_factory=list)
    blockers: list[Blocker] = Field(default_factory=list)
    checklist: list[ChecklistItem] = Field(default_factory=list)
    execution_plan: ExecutionPlan | None = None
    draft_status_update: str | None = None
    assumptions: list[str] = Field(default_factory=list)
    missing_info: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)

    @field_validator("summary")
    @classmethod
    def summary_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("summary must not be empty")
        return value


class WorkflowRun(BaseModel):
    run_id: UUID
    input: ProjectNote
    status: WorkflowStatus = WorkflowStatus.pending
    steps: list[WorkflowStep] = Field(default_factory=list)
    final_report: FinalReport | None = None
    created_at: datetime
    updated_at: datetime | None = None
