from datetime import datetime, timezone
from uuid import uuid4

from ai_workflow_assistant.domain.enums import StepStatus, WorkflowStatus
from ai_workflow_assistant.domain.models import ProjectNote, WorkflowRun, WorkflowStep
from ai_workflow_assistant.tools.errors import ToolNotFoundError
from ai_workflow_assistant.tools.models import ToolExecutionStatus
from ai_workflow_assistant.tools.registry import ToolRegistry

CLASSIFY_TOOL_NAME = "classify_project_note"


class WorkflowExecutor:
    def __init__(self, tool_registry: ToolRegistry) -> None:
        self._tool_registry = tool_registry

    def run(self, project_note: ProjectNote) -> WorkflowRun:
        created_at = datetime.now(timezone.utc)
        run = WorkflowRun(
            run_id=uuid4(),
            input=project_note,
            status=WorkflowStatus.running,
            created_at=created_at,
        )

        try:
            result = self._tool_registry.execute(
                CLASSIFY_TOOL_NAME,
                {"content": project_note.content},
            )
        except ToolNotFoundError:
            step = WorkflowStep(
                name=CLASSIFY_TOOL_NAME,
                tool_name=CLASSIFY_TOOL_NAME,
                status=StepStatus.failed,
                error=f"Required tool '{CLASSIFY_TOOL_NAME}' was not found",
            )
            return run.model_copy(
                update={
                    "status": WorkflowStatus.failed,
                    "steps": [step],
                    "updated_at": datetime.now(timezone.utc),
                }
            )

        if result.status == ToolExecutionStatus.success:
            category = getattr(result.output, "category", "unknown")
            step = WorkflowStep(
                name=CLASSIFY_TOOL_NAME,
                tool_name=CLASSIFY_TOOL_NAME,
                status=StepStatus.completed,
                summary=f"Classified project note as {category}",
            )
            return run.model_copy(
                update={
                    "status": WorkflowStatus.completed,
                    "steps": [step],
                    "updated_at": datetime.now(timezone.utc),
                }
            )

        step = WorkflowStep(
            name=CLASSIFY_TOOL_NAME,
            tool_name=CLASSIFY_TOOL_NAME,
            status=StepStatus.failed,
            error=result.error or "Tool execution failed",
        )
        return run.model_copy(
            update={
                "status": WorkflowStatus.failed,
                "steps": [step],
                "updated_at": datetime.now(timezone.utc),
            }
        )
