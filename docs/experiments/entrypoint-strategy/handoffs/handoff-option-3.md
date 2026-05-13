> Historical note: This document predates the Stage 7 command surface redesign. Command examples may use legacy forms. Current canonical commands are `tul show`, `tul package`, `tul update`, `tul verify`, `tul export`, `tul run`, `tul clean`, `tul recover`, and `tul setup`.

# Option 3 full handoff example

Mode: post-update
Project: tul
Branch: main
HEAD: <runtime-commit-hash>
Remote HEAD after fetch: <runtime-remote-head>
Push verified: <true|false>
Working tree: <clean|dirty>
State: <state-path>
Report: <report-path>
Rollback: git revert <runtime-commit-hash> && git push origin main

## Full embedded protocol

`tul update <project>` is the default full-loop command. Push is included by default. `--no-push` and `--no-commit` are exceptions. `git add -A` and `git add .` are forbidden. Force push is forbidden. Project policy belongs in `.tul.yml`. Environment paths and aliases belong in global config. LLM packages should use `tul-package.yml + files/ + README.md`.

The receiving LLM must verify remote state if possible, read relevant repo files, preserve invariants, identify structural debt, and propose the next package boundary.

## Durable repo pointers

- `README.md`
- `docs/llm/entrypoint.md`
- `docs/status/current.md`
- `docs/roadmap.md`
- `docs/checklists/loop-runtime.md`
- `docs/protocols/command-grammar.md`
- `docs/protocols/llm-handoff-protocol.md`
- `templates/project-instructions.md`

## Risk note

This handoff is self-contained but repeats durable protocol text. It is useful for disconnected review, but it increases output length and duplication.
