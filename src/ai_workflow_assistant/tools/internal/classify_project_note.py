from pydantic import BaseModel, field_validator

from ai_workflow_assistant.tools.models import RegisteredTool

BLOCKER_KEYWORDS = ("blocked", "blocker", "waiting", "issue", "problem")
DELIVERY_KEYWORDS = ("demo", "ship", "release", "deadline")


class ClassifyProjectNoteInput(BaseModel):
    content: str

    @field_validator("content")
    @classmethod
    def content_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("content must not be empty or whitespace-only")
        return value


class ClassifyProjectNoteOutput(BaseModel):
    category: str
    confidence: float
    reason: str

    @field_validator("category", "reason")
    @classmethod
    def text_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("must not be empty")
        return value

    @field_validator("confidence")
    @classmethod
    def confidence_must_be_in_range(cls, value: float) -> float:
        if not 0.0 <= value <= 1.0:
            raise ValueError("confidence must be between 0 and 1")
        return value


def classify_project_note(
    payload: ClassifyProjectNoteInput,
) -> ClassifyProjectNoteOutput:
    content_lower = payload.content.lower()

    if any(keyword in content_lower for keyword in BLOCKER_KEYWORDS):
        return ClassifyProjectNoteOutput(
            category="planning_with_blockers",
            confidence=0.8,
            reason="Content mentions blockers or problems that may impede progress.",
        )

    if any(keyword in content_lower for keyword in DELIVERY_KEYWORDS):
        return ClassifyProjectNoteOutput(
            category="delivery_planning",
            confidence=0.75,
            reason="Content focuses on delivery, demo, release, or deadline work.",
        )

    return ClassifyProjectNoteOutput(
        category="general_planning",
        confidence=0.6,
        reason="Content did not match blocker or delivery keyword patterns.",
    )


def build_classify_project_note_tool() -> RegisteredTool:
    return RegisteredTool(
        name="classify_project_note",
        description=(
            "Deterministically classify a project note into a planning category "
            "using simple keyword rules."
        ),
        input_model=ClassifyProjectNoteInput,
        output_model=ClassifyProjectNoteOutput,
        handler=classify_project_note,
    )
