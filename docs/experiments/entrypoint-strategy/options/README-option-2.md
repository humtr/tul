> Historical note: This document predates the Stage 7 command surface redesign. Command examples may use legacy forms. Current canonical commands are `tul show`, `tul package`, `tul update`, `tul verify`, `tul export`, `tul run`, `tul clean`, `tul recover`, and `tul setup`.

# Option 2 — README brief + dedicated handoff

## LLM entrypoint

If you are an LLM, coding agent, or a new session reviewing this repo, start here:

1. Read `docs/llm/entrypoint.md`.
2. Read `docs/status/current.md`.
3. Read `docs/roadmap.md`.
4. Read `docs/checklists/loop-runtime.md`.
5. Read `docs/protocols/llm-handoff-protocol.md` if handling a handoff.
6. Read `docs/protocols/command-grammar.md` if interpreting `/tul ...` commands.

## Project identity

`tul` means Terminal Update Loop. It is a cross-platform loop runtime for applying LLM-generated packages, validating them, committing, pushing, verifying remote HEAD, printing rollback guidance, and generating an LLM-ready handoff.

## Non-negotiable invariants

- `tul update <project>` is the default full-loop command.
- Push is included by default.
- `--no-push` and `--no-commit` are exceptions.
- Remote HEAD verification is part of successful update.
- Do not use `git add -A` or `git add .`.
- Do not force push.
- Project policy belongs in `.tul.yml`.
- Environment paths and aliases belong in global config.
- LLM packages should use `tul-package.yml + files/ + README.md`.

## Current checkpoint

Latest verified stage at the time of this experiment:

- Stage 1.5 — no-op/state cleanup.
- Latest verified commit: `42c77b0 Handle no-op updates and archive state`.
- Next stage: Stage 2 — LLM loop contract.

For the maintained status source, read `docs/status/current.md`.
For the maintained roadmap, read `docs/roadmap.md`.

## Runtime facts

Do not treat README text as proof that a package was applied or pushed. Runtime facts belong in `tul handoff` output:

- commit hash;
- push verified;
- remote HEAD after fetch;
- rollback command;
- state path;
- report path;
- working tree status.

Use compact handoff by default. Use `tul handoff --full` only when the receiving LLM needs the complete protocol text.

## Recommended LLM-side commands

- `/tul next <project>` — propose the next package scope.
- `/tul review <project>` — review the pushed commit/handoff.
- `/tul package <project>` — generate the next cross-platform tul package.
- `/tul roadmap <project>` — update roadmap/status/checklist.
- `/tul verify <project>` — verify repo consistency with handoff/protocol/roadmap.
- `/tul init-review <project>` — perform first review after clone/init.

## Why this option exists

This option keeps README small enough for reliable first contact while placing detailed and changing information in dedicated docs and handoff output.
