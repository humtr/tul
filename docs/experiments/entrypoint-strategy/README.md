> Historical note: This document predates the Stage 7 command surface redesign. Command examples may use legacy forms. Current canonical commands are `tul show`, `tul package`, `tul update`, `tul verify`, `tul export`, `tul run`, `tul clean`, `tul recover`, and `tul setup`.

# LLM entrypoint strategy test

Status: experiment package
Stage: pre-implementation validation for Stage 2 — LLM loop contract
Commit intent: add testable strategy documents, not production behavior

## Problem

The tul repo must be readable by a new LLM, another session, or a coding agent without relying on prior chat context. The first file that most agents inspect is `README.md`, but runtime handoff also needs to carry facts that are only known after an update has run.

This experiment compares three strategies:

1. **README-only**: put all LLM onboarding, status, roadmap, invariants, and next-step guidance directly in `README.md`.
2. **README brief + dedicated handoff**: keep README short but include init/status pointers and current stage summary; put runtime facts in compact/full handoff output and durable details in repo docs.
3. **README comprehensive + dedicated handoff**: include almost all onboarding material in README and also provide dedicated handoff output.

## Background included in this test

This experiment explicitly accounts for the recent confusion about repository access:

- Web/raw views can make a file appear collapsed or misleading.
- File-by-file GitHub blob review is still useful.
- Full clone/download may be unavailable to some assistant runtimes.
- Execution-level validation still requires fresh clone or terminal evidence such as `wc -l`, `py_compile`, and `git diff --check`.
- README should therefore act as a stable LLM entrypoint, but it should not become the only source of truth for runtime facts.

## Tested options

- `options/README-option-1.md`
- `options/README-option-2.md`
- `options/README-option-3.md`
- `handoffs/handoff-option-2.md`
- `handoffs/handoff-option-3.md`

## Evaluation documents

- `test-protocol.md`: how to test the options after this commit is pushed.
- `evaluation-matrix.md`: criteria and preliminary scoring.
- `recommendation.md`: recommended next production package boundary.

## Expected outcome

The expected result is that Option 2 becomes the production design:

- README remains a stable entrypoint.
- Runtime handoff remains compact by default.
- `tul handoff --full` provides the full protocol.
- `tul instructions` or `tul handoff --instructions` prints project instructions.
- Current state and roadmap live in durable repo docs.
