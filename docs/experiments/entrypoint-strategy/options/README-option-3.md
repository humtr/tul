> Historical note: This document predates the Stage 7 command surface redesign. Command examples may use legacy forms. Current canonical commands are `tul show`, `tul package`, `tul update`, `tul verify`, `tul export`, `tul run`, `tul clean`, `tul recover`, and `tul setup`.

# Option 3 — README comprehensive + dedicated handoff

## LLM entrypoint

This README is intended to be self-sufficient for a new LLM or coding agent. It also points to dedicated durable docs and handoff outputs.

Read order:

1. This README.
2. `docs/llm/entrypoint.md`.
3. `docs/status/current.md`.
4. `docs/roadmap.md`.
5. `docs/checklists/loop-runtime.md`.
6. `docs/protocols/llm-handoff-protocol.md`.
7. `templates/project-instructions.md`.

## Project identity

`tul` means Terminal Update Loop. It exists to reduce human bridge work between LLM package generation and terminal/GitHub execution.

## Core loop

```text
LLM creates package
→ user downloads package
→ tul update <project>
→ package discovery/import
→ manifest validation
→ safe apply
→ repo check
→ sweep
→ explicit stage
→ staged check
→ commit
→ push
→ remote HEAD verification
→ rollback hint
→ report
→ compact handoff
→ next LLM reviews remote and proposes next package
```

## Invariants

- `tul update <project>` is the default full-loop command.
- Push is included by default.
- `--no-push` and `--no-commit` are exceptions.
- Remote HEAD verification is required for successful update.
- Do not use `git add -A` or `git add .`.
- Do not force push.
- Default rollback is `git revert <commit>` followed by `git push origin <branch>`.
- Project-specific policy belongs in `.tul.yml`.
- Environment paths and project aliases belong in global config.
- LLM-generated packages should be cross-platform `tul-package.yml + files/ + README.md` packages.
- Windows/Termux package flow should converge.

## Current status

Latest verified stage at the time of this experiment:

- Stage 0 — syntax/runtime recovery: complete.
- Stage 1 — runtime boundary restructure: complete.
- Stage 1.5 — no-op/state cleanup: complete.
- Stage 2 — LLM loop contract: next.

Latest verified commit:

- `42c77b0 Handle no-op updates and archive state`.

## Current roadmap

Stage 2 — LLM loop contract:

- Add compact handoff default.
- Add `tul handoff --full`.
- Add `tul handoff --instructions`.
- Add `tul instructions`.
- Add durable docs under `docs/llm`, `docs/status`, `docs/roadmap`, and `docs/checklists`.

Stage 2.5 — apply safety audit:

- Restrict directory copy.
- Add apply plan logging.
- Align manifest apply destinations with commit allowlist.

Stage 3 — recovery/debug commands.
Stage 4 — init/config onboarding.
Stage 5 — `humtr/ai` onboarding.
Stage 6 — self-host loop hardening.

## Runtime handoff

Runtime handoff carries facts that README cannot know ahead of time:

- commit hash;
- push verification result;
- remote HEAD;
- rollback command;
- state/report/handoff paths;
- working tree status.

Default handoff should be compact. `--full` should include the full protocol.

## Risks

This option maximizes standalone readability but duplicates status and roadmap content. It has the highest staleness risk and can make README too large for quick agent orientation.
