from datetime import datetime, timezone
from uuid import uuid4

import pytest
from pydantic import ValidationError

from ai_workflow_assistant.domain.enums import Priority, StepStatus, WorkflowStatus
from ai_workflow_assistant.domain.models import (
    ActionItem,
    Blocker,
    ChecklistItem,
    ExecutionPlan,
    FinalReport,
    ProjectNote,
    WorkflowRun,
    WorkflowStep,
)
from ai_workflow_assistant.schemas.workflow import WorkflowRunRequest


def test_project_note_rejects_empty_content() -> None:
    with pytest.raises(ValidationError):
        ProjectNote(content="")


def test_project_note_rejects_whitespace_only_content() -> None:
    with pytest.raises(ValidationError):
        ProjectNote(content="   ")


def test_workflow_run_request_rejects_empty_content() -> None:
    with pytest.raises(ValidationError):
        WorkflowRunRequest(content="")


def test_action_item_accepts_minimal_valid_data() -> None:
    item = ActionItem(description="Ship health endpoint")

    assert item.description == "Ship health endpoint"
    assert item.priority == Priority.medium
    assert item.tags == []
    assert item.missing_info == []
    assert item.confidence is None


def test_action_item_rejects_confidence_out_of_range() -> None:
    with pytest.raises(ValidationError):
        ActionItem(description="Task", confidence=-0.1)

    with pytest.raises(ValidationError):
        ActionItem(description="Task", confidence=1.1)


def test_action_item_rejects_whitespace_only_description() -> None:
    with pytest.raises(ValidationError):
        ActionItem(description="   ")


def test_action_item_list_defaults_are_not_shared() -> None:
    first = ActionItem(description="First task")
    second = ActionItem(description="Second task")

    first.tags.append("backend")
    first.missing_info.append("owner")

    assert second.tags == []
    assert second.missing_info == []
    assert first.tags is not second.tags
    assert first.missing_info is not second.missing_info


def test_blocker_rejects_confidence_out_of_range() -> None:
    with pytest.raises(ValidationError):
        Blocker(description="Blocked on review", confidence=-0.1)

    with pytest.raises(ValidationError):
        Blocker(description="Blocked on review", confidence=1.1)


def test_blocker_rejects_whitespace_only_description() -> None:
    with pytest.raises(ValidationError):
        Blocker(description="   ")


def test_checklist_item_rejects_whitespace_only_description() -> None:
    with pytest.raises(ValidationError):
        ChecklistItem(description="   ")


def test_execution_plan_rejects_empty_objective() -> None:
    with pytest.raises(ValidationError):
        ExecutionPlan(objective="")


def test_execution_plan_rejects_empty_step_strings() -> None:
    with pytest.raises(ValidationError):
        ExecutionPlan(objective="Finish P2", steps=["Write models", "  "])


def test_final_report_can_include_structured_sections() -> None:
    report = FinalReport(
        summary="P2 domain models are ready for review",
        action_items=[ActionItem(description="Review domain models")],
        blockers=[Blocker(description="Waiting on design feedback")],
        checklist=[ChecklistItem(description="Add validation tests")],
        assumptions=["due_date stays a free-form string for now"],
        missing_info=["owner for follow-up tasks"],
    )

    assert report.overall_priority == Priority.medium
    assert len(report.action_items) == 1
    assert len(report.blockers) == 1
    assert len(report.checklist) == 1
    assert report.assumptions == ["due_date stays a free-form string for now"]
    assert report.missing_info == ["owner for follow-up tasks"]


def test_final_report_rejects_whitespace_only_summary() -> None:
    with pytest.raises(ValidationError):
        FinalReport(summary="   ")


def test_workflow_run_can_represent_pending_run_without_final_report() -> None:
    run = WorkflowRun(
        run_id=uuid4(),
        input=ProjectNote(content="Need to finish domain models"),
        created_at=datetime.now(timezone.utc),
    )

    assert run.status == WorkflowStatus.pending
    assert run.steps == []
    assert run.final_report is None
    assert run.updated_at is None


def test_workflow_step_can_represent_failed_step_with_error() -> None:
    step = WorkflowStep(
        name="extract_action_items",
        status=StepStatus.failed,
        tool_name="extract_action_items",
        error="tool raised ValueError",
    )

    assert step.status == StepStatus.failed
    assert step.error == "tool raised ValueError"


def test_workflow_step_rejects_whitespace_only_name() -> None:
    with pytest.raises(ValidationError):
        WorkflowStep(name="   ")
