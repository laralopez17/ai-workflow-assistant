# AI Workflow Assistant

A backend-first AI agent workflow system that turns messy project notes into structured execution plans.

## Why this project matters

Many AI demos look impressive in a chat window but are hard to test, audit, or reuse. This project focuses on the engineering behind agent systems: controlled tool calling, workflow traces, structured outputs, and persistence.

It complements a previous portfolio project, [ai-repository-assistant](https://github.com/laralopez17/ai-repository-assistant), which demonstrated RAG, embeddings, semantic search, and source-grounded answers. Together they show two sides of applied AI:

- **Retrieval and grounding** — find and cite relevant context
- **Agent workflows** — plan, call tools safely, execute steps, and return structured results

## Planned v1 capabilities

- Accept messy project notes as input
- Classify notes and extract action items
- Identify blockers and estimate priority
- Create a structured execution plan
- Draft a status update from the plan
- Validate workflow output before returning a final result
- Keep a full workflow trace for each run
- Persist runs for later inspection
- Support fake providers for deterministic tests
- Optionally use an OpenAI provider for live demos

## Planned architecture

```
API (FastAPI) → Services → Agent / Workflow Engine → Registered Tools → Providers
                              ↓
                         Trace + Persistence
```

- **Routes** stay thin and only handle HTTP concerns
- **Services** own business logic and orchestration
- **Domain models** stay independent from FastAPI
- **Tools** are controlled internal capabilities registered by the application
- **Providers** abstract LLM access (fake for tests, optional OpenAI for demos)
- **Traces** record planning, tool calls, and outcomes for every run

## v1 scope

v1 uses **controlled internal tools**, not external integrations.

Internal tools are real application capabilities, for example:

- `classify_project_note`
- `extract_action_items`
- `identify_blockers`
- `estimate_priority`
- `create_execution_plan`
- `draft_status_update`
- `validate_workflow_output`

The system is intentionally not a magical autonomous agent. It is a controlled, testable backend where the agent can plan, call only registered tools, execute steps, keep a trace, persist the run, and return a structured final result.

## Out of scope (v1)

- External integrations (GitHub Issues, Gmail, Calendar, Slack, etc.)
- Fully autonomous multi-agent swarms
- Frontend UI beyond what is needed for demos later
- Production multi-tenant auth and billing
- Unbounded tool access to the public internet

## Milestone roadmap

| Milestone | Focus                                                                      |
| --------- | -------------------------------------------------------------------------- |
| **P0**    | AI-assisted workflow setup — docs, guidance, `.gitignore`                  |
| **P1**    | Project skeleton — package layout, FastAPI app entry, config, health check |
| **P2**    | Domain models — notes, plans, traces, structured outputs (Pydantic)        |
| **P3**    | Tool registry — register and invoke internal tools safely                  |
| **P4**    | Workflow engine — plan → tool calls → validate → final result + trace      |
| **P5**    | Fake provider + tests — deterministic unit/API tests                       |
| **P6**    | Persistence — SQLite storage for runs and traces                           |
| **P7**    | Optional OpenAI provider — real demos behind a clear boundary              |
| **P8**    | Docker + polish — runnable demo, docs update, portfolio write-up           |

## Status

**P0 in progress** — initial documentation and project guidance.
