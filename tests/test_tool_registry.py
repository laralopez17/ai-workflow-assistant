import pytest
from pydantic import BaseModel

from ai_workflow_assistant.tools.errors import (
    ToolAlreadyRegisteredError,
    ToolNotFoundError,
)
from ai_workflow_assistant.tools.internal.classify_project_note import (
    ClassifyProjectNoteOutput,
    build_classify_project_note_tool,
)
from ai_workflow_assistant.tools.models import (
    RegisteredTool,
    ToolExecutionStatus,
)
from ai_workflow_assistant.tools.registry import ToolRegistry


class StubInput(BaseModel):
    value: str


class StubOutput(BaseModel):
    result: str


def _build_stub_tool(
    *,
    name: str = "stub_tool",
    handler,
) -> RegisteredTool:
    return RegisteredTool(
        name=name,
        description="Test-only stub tool",
        input_model=StubInput,
        output_model=StubOutput,
        handler=handler,
    )


def test_register_and_get_tool_by_name() -> None:
    registry = ToolRegistry()
    tool = build_classify_project_note_tool()

    registry.register(tool)

    assert registry.get("classify_project_note") is tool


def test_registering_same_tool_twice_raises() -> None:
    registry = ToolRegistry()
    tool = build_classify_project_note_tool()
    registry.register(tool)

    with pytest.raises(ToolAlreadyRegisteredError):
        registry.register(tool)


def test_getting_unknown_tool_raises() -> None:
    registry = ToolRegistry()

    with pytest.raises(ToolNotFoundError):
        registry.get("missing_tool")


def test_executing_unknown_tool_raises() -> None:
    registry = ToolRegistry()

    with pytest.raises(ToolNotFoundError):
        registry.execute("missing_tool", {"content": "hello"})


def test_classify_project_note_detects_blockers() -> None:
    registry = ToolRegistry()
    registry.register(build_classify_project_note_tool())

    result = registry.execute(
        "classify_project_note",
        {"content": "We are blocked waiting on review for this issue"},
    )

    assert result.status == ToolExecutionStatus.success
    assert isinstance(result.output, ClassifyProjectNoteOutput)
    assert result.output.category == "planning_with_blockers"


def test_classify_project_note_detects_delivery() -> None:
    registry = ToolRegistry()
    registry.register(build_classify_project_note_tool())

    result = registry.execute(
        "classify_project_note",
        {"content": "Need to ship the demo before the release deadline"},
    )

    assert result.status == ToolExecutionStatus.success
    assert isinstance(result.output, ClassifyProjectNoteOutput)
    assert result.output.category == "delivery_planning"


def test_classify_project_note_defaults_to_general_planning() -> None:
    registry = ToolRegistry()
    registry.register(build_classify_project_note_tool())

    result = registry.execute(
        "classify_project_note",
        {"content": "Capture notes from today's standup"},
    )

    assert result.status == ToolExecutionStatus.success
    assert isinstance(result.output, ClassifyProjectNoteOutput)
    assert result.output.category == "general_planning"


def test_invalid_input_returns_failed_result() -> None:
    registry = ToolRegistry()
    registry.register(build_classify_project_note_tool())

    result = registry.execute("classify_project_note", {"content": "   "})

    assert result.status == ToolExecutionStatus.failed
    assert result.output is None
    assert result.error is not None
    assert "\n" not in result.error


def test_handler_exception_returns_failed_result() -> None:
    def boom(_payload: StubInput) -> StubOutput:
        raise RuntimeError("handler exploded")

    registry = ToolRegistry()
    registry.register(_build_stub_tool(handler=boom))

    result = registry.execute("stub_tool", {"value": "ok"})

    assert result.status == ToolExecutionStatus.failed
    assert result.error == "handler exploded"
    assert result.output is None


def test_invalid_handler_output_returns_failed_result() -> None:
    class WrongOutput(BaseModel):
        unexpected: int

    def bad_handler(_payload: StubInput) -> WrongOutput:
        return WrongOutput(unexpected=1)

    registry = ToolRegistry()
    registry.register(_build_stub_tool(handler=bad_handler))

    result = registry.execute("stub_tool", {"value": "ok"})

    assert result.status == ToolExecutionStatus.failed
    assert result.output is None
    assert result.error is not None


def test_list_tools_preserves_registration_order() -> None:
    registry = ToolRegistry()
    first = _build_stub_tool(name="alpha", handler=lambda p: StubOutput(result=p.value))
    second = build_classify_project_note_tool()

    registry.register(first)
    registry.register(second)

    names = [tool.name for tool in registry.list_tools()]
    assert names == ["alpha", "classify_project_note"]


def test_tool_names_are_matched_exactly() -> None:
    registry = ToolRegistry()
    registry.register(build_classify_project_note_tool())

    with pytest.raises(ToolNotFoundError):
        registry.get("Classify_Project_Note")
