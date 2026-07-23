# Project Notes — AI Workflow Assistant

## Project goal

Build a backend-first AI agent workflow system that turns messy project notes into structured execution plans, with controlled tool calling, workflow traces, structured outputs, and persistence.

## Portfolio positioning

This is **Project Horizon — Project 2**.

It complements `ai-repository-assistant` (Project 1), which focused on RAG, embeddings, semantic search, and source-grounded answers.

| Project | Demonstrates |
|---------|----------------|
| `ai-repository-assistant` | Retrieval, embeddings, semantic search, grounded Q&A |
| `ai-workflow-assistant` | Agent architecture, tool calling, traces, structured workflows |

Together they show both **finding relevant context** and **acting on it through a controlled agent pipeline**.

## Stack decision

| Layer | Choice | Notes |
|-------|--------|--------|
| Language | Python | Clear fit for AI/backend portfolio work |
| API | FastAPI | Thin routes, OpenAPI, async-friendly |
| Validation | Pydantic | Structured inputs/outputs and domain models |
| Tests | pytest | Service and API behavior tests |
| Persistence | SQLite (later) | Simple local persistence for runs/traces |
| Packaging | Docker (later) | Reproducible demos |
| LLM | Fake providers first; OpenAI optional later | Deterministic tests; real demos when needed |

## Scope rule

**v1 = controlled internal tools only.**

Internal tools are application capabilities (classify, extract, prioritize, plan, draft, validate). External systems (GitHub, Gmail, Calendar, Slack, etc.) are **post-v1** ideas, not v1 requirements.

Do not expand scope into integrations, UI product work, or autonomous multi-agent systems during v1 milestones.

## v1 product idea

A developer pastes messy project notes (standup scraps, Slack dumps, half-written tickets). The system:

1. Classifies the note
2. Extracts action items
3. Identifies blockers
4. Estimates priority
5. Builds an execution plan
6. Drafts a status update
7. Validates the structured output
8. Returns a final result with a full workflow trace
9. Persists the run for inspection

Every tool call is registered, logged, and testable. Fake providers keep CI deterministic; an optional OpenAI provider supports live demos.

## Initial milestone plan

1. **P0** — Docs and agent guidance — **complete**
2. **P1** — FastAPI skeleton, config, health endpoint — **complete**
3. **P2** — Domain models and structured schemas — **complete**
4. **P3** — Internal tool registry and safe invocation — **complete**
5. **P4** — Workflow engine with planning, execution, and traces
6. **P5** — Fake LLM/provider + pytest coverage
7. **P6** — SQLite persistence for runs and traces
8. **P7** — Optional OpenAI provider for demos
9. **P8** — Docker, docs polish, portfolio narrative

## P1 — FastAPI skeleton

P1 establishes the backend foundation only:

- `src/` layout with package `ai_workflow_assistant`
- `pyproject.toml` for packaging and dependencies (FastAPI, uvicorn, pydantic, pydantic-settings)
- Centralized settings via `pydantic-settings` (`APP_NAME`, `APP_VERSION`, `ENVIRONMENT`)
- Thin health route at `GET /health`
- pytest coverage for the health endpoint using FastAPI's `TestClient`

No agent logic, tool registry, workflow engine, LLM providers, or persistence was added in P1.

## P2 — Domain models and API schemas

P2 defines the data contracts and domain vocabulary only:

- Domain enums: `Priority`, `TaskStatus`, `WorkflowStatus`, `StepStatus`
- Domain models: `ProjectNote`, `ActionItem`, `Blocker`, `ChecklistItem`, `ExecutionPlan`, `WorkflowStep`, `FinalReport`, `WorkflowRun`
- API schemas: `WorkflowRunRequest`, `WorkflowRunResponse` (no endpoint yet)
- Validation tests for empty content, invalid confidence, and core construction paths

Decisions recorded in P2:

- **Content-only input for v1** — the user provides `content`; title, project name, and requested output are not required
- **Structured outputs** — the system returns typed models (`FinalReport`, `ActionItem`, etc.), not generic free text
- **`missing_info` and `assumptions`** — models surface gaps instead of inventing missing details
- **Workflow traces are part of the design** — `WorkflowRun.steps` holds `WorkflowStep` entries for auditability
- **Tool registry deferred to P3** — `WorkflowStep.tool_name` is a minimal hook; deep `ToolCallTrace` waits for later milestones

## P3 — Internal tool registry

P3 adds tool infrastructure only:

- `ToolRegistry` for exact-name register/get/list/execute
- `RegisteredTool` with structured input/output models and an `execute` method
- Custom errors: `ToolAlreadyRegisteredError`, `ToolNotFoundError`
- Structured `ToolExecutionResult` for success and failure paths
- One deterministic example tool: `classify_project_note`

Decisions recorded in P3:

- **Registry before workflow execution** — tools exist as an explicit capability layer first
- **Tools are explicit and controlled** — only registered tools can be invoked; names match exactly
- **Input/output validation** — Pydantic models constrain tool I/O before any LLM planner exists
- **Structured execution errors** — validation/handler failures return failed results with concise messages (no stack traces); unknown tools still raise
- **`classify_project_note` is architectural scaffolding** — keyword rules only; not real AI intelligence
- **Executor and LLM planner deferred** — no `/workflows/run`, no providers, no persistence in P3

## Learning goals

- Design a small agent system that is controllable and testable
- Separate domain logic from framework (FastAPI) concerns
- Implement tool registration and controlled execution
- Capture workflow traces as first-class artifacts
- Use fake providers so tests do not depend on live APIs
- Persist runs without over-engineering storage
- Practice AI-assisted development with clear milestones and review

## Post-v1 future ideas

- GitHub Issues sync (create/update issues from plans)
- Gmail or email draft delivery
- Calendar blockers / scheduling hints
- Slack status posts
- Multi-step human approval gates
- Richer frontend for inspecting traces
- Multi-user auth and project workspaces
