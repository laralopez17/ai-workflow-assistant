from datetime import datetime, timezone

from pydantic import BaseModel

from ai_workflow_assistant.domain.enums import StepStatus, WorkflowStatus
from ai_workflow_assistant.domain.models import ProjectNote
from ai_workflow_assistant.tools.internal.classify_project_note import (
    build_classify_project_note_tool,
)
from ai_workflow_assistant.tools.models import RegisteredTool
from ai_workflow_assistant.tools.registry import ToolRegistry
from ai_workflow_assistant.workflows.executor import WorkflowExecutor


class ClassifyInput(BaseModel):
    content: str


class ClassifyOutput(BaseModel):
    category: str
    confidence: float
    reason: str


def _failing_classify_tool() -> RegisteredTool:
    def boom(_payload: ClassifyInput) -> ClassifyOutput:
        raise RuntimeError("classification failed")

    return RegisteredTool(
        name="classify_project_note",
        description="Test-only failing classify tool",
        input_model=ClassifyInput,
        output_model=ClassifyOutput,
        handler=boom,
    )


def test_executor_completes_run_when_classify_succeeds() -> None:
    registry = ToolRegistry()
    registry.register(build_classify_project_note_tool())
    executor = WorkflowExecutor(tool_registry=registry)

    run = executor.run(ProjectNote(content="Capture notes from today's standup"))

    assert run.status == WorkflowStatus.completed
    assert len(run.steps) == 1
    step = run.steps[0]
    assert step.status == StepStatus.completed
    assert step.name == "classify_project_note"
    assert step.tool_name == "classify_project_note"
    assert run.final_report is None


def test_executor_summary_includes_delivery_planning_category() -> None:
    registry = ToolRegistry()
    registry.register(build_classify_project_note_tool())
    executor = WorkflowExecutor(tool_registry=registry)

    run = executor.run(
        ProjectNote(content="We need to prepare the demo before the deadline")
    )

    assert run.status == WorkflowStatus.completed
    assert run.steps[0].summary is not None
    assert "delivery_planning" in run.steps[0].summary


def test_executor_fails_when_required_tool_is_missing() -> None:
    executor = WorkflowExecutor(tool_registry=ToolRegistry())

    run = executor.run(ProjectNote(content="Need a classification"))

    assert run.status == WorkflowStatus.failed
    assert len(run.steps) == 1
    step = run.steps[0]
    assert step.status == StepStatus.failed
    assert step.error is not None
    assert "classify_project_note" in step.error
    assert "not found" in step.error.lower()


def test_executor_fails_when_tool_execution_fails() -> None:
    registry = ToolRegistry()
    registry.register(_failing_classify_tool())
    executor = WorkflowExecutor(tool_registry=registry)

    run = executor.run(ProjectNote(content="Anything"))

    assert run.status == WorkflowStatus.failed
    assert len(run.steps) == 1
    step = run.steps[0]
    assert step.status == StepStatus.failed
    assert step.error == "classification failed"


def test_executor_sets_timezone_aware_timestamps() -> None:
    registry = ToolRegistry()
    registry.register(build_classify_project_note_tool())
    executor = WorkflowExecutor(tool_registry=registry)

    run = executor.run(ProjectNote(content="Ship the release"))

    assert isinstance(run.created_at, datetime)
    assert run.created_at.tzinfo is not None
    assert run.updated_at is not None
    assert run.updated_at.tzinfo is not None
    assert run.updated_at.utcoffset() == timezone.utc.utcoffset(None)


def test_executor_does_not_generate_final_report() -> None:
    registry = ToolRegistry()
    registry.register(build_classify_project_note_tool())
    executor = WorkflowExecutor(tool_registry=registry)

    run = executor.run(ProjectNote(content="General planning notes"))

    assert run.final_report is None
