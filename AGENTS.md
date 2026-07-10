# AGENTS.md

Guidance for AI coding agents working in this repository.

## Role

You are assisting a human developer building **AI Workflow Assistant** — a controlled, testable backend agent workflow system. Prefer clarity, small milestones, and reviewable diffs over speed.

## Before coding

- Always explain the plan before coding.
- Confirm which milestone is in scope.
- List files you expect to create or change.
- Call out risks, assumptions, and anything intentionally left out.

## Milestone discipline

- Keep milestones small.
- Do not implement features outside the current milestone.
- Do not introduce external integrations in v1.
- Prefer incremental, reviewable changes over large multi-concern PRs.

## Dependencies

- Do not add dependencies without explaining why.
- Prefer the standard library and already-chosen stack (FastAPI, Pydantic, pytest) unless a new library clearly reduces risk or complexity.
- Avoid speculative packages “for later.”

## Architecture

- Keep routes thin.
- Keep business logic in services.
- Keep domain models independent from FastAPI.
- Prefer explicit, readable code over clever abstractions.
- Respect a clear separation: API → services → domain/tools/providers → persistence.

## Tools and providers

- v1 tools are internal application capabilities only.
- Do not wire GitHub, Gmail, Calendar, Slack, or other external systems in v1.
- Do not call real external APIs in tests.
- Use fake providers for deterministic tests.
- Keep any optional OpenAI (or other live) provider behind a clear boundary and out of default test paths.

## Testing

- Write tests for services and API behavior.
- Prefer deterministic fixtures and fake providers.
- Cover happy paths and important failure/validation cases for the current milestone.
- Do not require network access or live LLM keys for the test suite.

## Documentation

- Update documentation after each milestone.
- Keep `README.md` status and roadmap accurate.
- Capture decisions and scope changes in `PROJECT_NOTES.md` when they matter for portfolio narrative or future work.

## Git and review

- The human developer must review diffs before committing.
- Do not commit unless the human explicitly asks.
- Do not push unless the human explicitly asks.
- Do not amend shared history or force-push unless explicitly requested.

## Code style

- Avoid obvious comments. Use short comments only when they clarify non-trivial workflow, agent, or tool execution logic.
- Match existing project conventions once application code exists.
- Avoid drive-by refactors unrelated to the current milestone.
- Do not add unused abstractions, config flags, or “flexibility” that the current milestone does not need.
