# tul roadmap

## Stage 0 — Syntax/runtime recovery

Status: done.

Related commit: `d79f288 Hotfix tul runtime syntax and newlines`

## Stage 1 — Runtime boundary restructure

Status: done.

Related commit: `86fa990 Restructure tul update runtime boundaries`

## Stage 1.5 — No-op/state cleanup

Status: done.

Related commit: `42c77b0 Handle no-op updates and archive state`

## Stage 2 — LLM loop contract

Status: active.

Goals:

- Add `docs/llm/entrypoint.md`.
- Add LLM-side command grammar.
- Add durable status, roadmap, and checklist documents.
- Make compact handoff the default.
- Add `tul handoff --full`.
- Add `tul handoff --instructions` and `tul instructions`.
- Keep update-success auto handoff compact.

## Stage 2.5 — Apply safety audit

Goals:

- Restrict or explicitly gate directory copy.
- Record apply plans.
- Compare apply destinations with manifest `commit.files` before staging.
- Preserve path traversal protections.

## Stage 3 — Recovery/debug commands

Goals:

- Improve `state`, `archive`, `rollback`, `import`, and `apply` for recovery.
- Keep split commands out of the default workflow.

## Stage 4 — Init/config onboarding

Goals:

- Make `tul init tul` and `tul init ai` create or repair global config.
- Register aliases.
- Generate or patch `.tul.yml`.
- Generate initial-review handoff.

## Stage 5 — `humtr/ai` onboarding

Goals:

- Bring `humtr/ai` under tul loop control.
- Define branch policy, checks, and forbidden patterns in the target repo's `.tul.yml`.

## Stage 6 — Self-host loop hardening

Goals:

- Make repeated `tul update tul` and `tul update ai` safe, inspectable, and recoverable across Windows and Termux.
