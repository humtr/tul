> Historical note: This document predates the Stage 7 command surface redesign. Command examples may use legacy forms. Current canonical commands are `tul show`, `tul package`, `tul update`, `tul verify`, `tul export`, `tul run`, `tul clean`, `tul recover`, and `tul setup`.

# Option 2 compact handoff example

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

## Repo pointers

- LLM entrypoint: `docs/llm/entrypoint.md`
- Current status: `docs/status/current.md`
- Roadmap: `docs/roadmap.md`
- Checklist: `docs/checklists/loop-runtime.md`
- Command grammar: `docs/protocols/command-grammar.md`
- Full handoff protocol: `docs/protocols/llm-handoff-protocol.md`
- Project instructions: `templates/project-instructions.md`

## Request to LLM

1. Verify the remote repo, branch, and expected HEAD if possible.
2. Read the repo pointers above before proposing implementation.
3. Preserve tul invariants.
4. Separate terminal-verified facts from assistant interpretation.
5. Propose the next package boundary.

Use `tul handoff --full` if the full protocol text is needed.
