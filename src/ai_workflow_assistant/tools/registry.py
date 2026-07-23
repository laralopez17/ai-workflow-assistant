from typing import Any

from pydantic import BaseModel

from ai_workflow_assistant.tools.errors import (
    ToolAlreadyRegisteredError,
    ToolNotFoundError,
)
from ai_workflow_assistant.tools.models import RegisteredTool, ToolExecutionResult


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, RegisteredTool] = {}

    def register(self, tool: RegisteredTool) -> None:
        if tool.name in self._tools:
            raise ToolAlreadyRegisteredError(
                f"tool already registered: {tool.name}"
            )
        self._tools[tool.name] = tool

    def get(self, name: str) -> RegisteredTool:
        try:
            return self._tools[name]
        except KeyError as exc:
            raise ToolNotFoundError(f"tool not found: {name}") from exc

    def list_tools(self) -> list[RegisteredTool]:
        return list(self._tools.values())

    def execute(
        self, name: str, raw_input: dict[str, Any] | BaseModel
    ) -> ToolExecutionResult:
        tool = self.get(name)
        return tool.execute(raw_input)
