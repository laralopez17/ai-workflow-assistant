from collections.abc import Callable
from enum import Enum
from typing import Any

from pydantic import BaseModel, ValidationError, field_validator


class ToolExecutionStatus(str, Enum):
    success = "success"
    failed = "failed"


class ToolExecutionResult(BaseModel):
    tool_name: str
    status: ToolExecutionStatus
    output: BaseModel | None = None
    error: str | None = None


class RegisteredTool(BaseModel):
    name: str
    description: str
    input_model: type[BaseModel]
    output_model: type[BaseModel]
    handler: Callable[[BaseModel], BaseModel]

    model_config = {"arbitrary_types_allowed": True}

    @field_validator("name", "description")
    @classmethod
    def must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("must not be empty")
        return value

    def execute(self, raw_input: dict[str, Any] | BaseModel) -> ToolExecutionResult:
        try:
            if isinstance(raw_input, self.input_model):
                validated_input = raw_input
            elif isinstance(raw_input, BaseModel):
                validated_input = self.input_model.model_validate(
                    raw_input.model_dump()
                )
            else:
                validated_input = self.input_model.model_validate(raw_input)

            handler_output = self.handler(validated_input)

            if isinstance(handler_output, self.output_model):
                validated_output = handler_output
            elif isinstance(handler_output, BaseModel):
                validated_output = self.output_model.model_validate(
                    handler_output.model_dump()
                )
            else:
                validated_output = self.output_model.model_validate(handler_output)

            return ToolExecutionResult(
                tool_name=self.name,
                status=ToolExecutionStatus.success,
                output=validated_output,
            )
        except ValidationError as exc:
            return ToolExecutionResult(
                tool_name=self.name,
                status=ToolExecutionStatus.failed,
                error=_concise_validation_error(exc),
            )
        except Exception as exc:
            return ToolExecutionResult(
                tool_name=self.name,
                status=ToolExecutionStatus.failed,
                error=str(exc) or exc.__class__.__name__,
            )


def _concise_validation_error(exc: ValidationError) -> str:
    errors = exc.errors()
    if not errors:
        return "validation failed"
    first = errors[0]
    location = ".".join(str(part) for part in first.get("loc", ()))
    message = first.get("msg", "validation failed")
    if location:
        return f"{location}: {message}"
    return message
