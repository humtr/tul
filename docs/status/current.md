# Current status

This document is the durable status surface for LLMs and coding agents. Runtime facts such as the exact current HEAD, push verification, and rollback command must still be read from `git log`, `git status`, and `tul handoff` output.

## Latest verified baseline before this adoption package

The user verified a fresh clone at:

```text
df84b64 Add LLM entrypoint strategy test
de13ecd Stabilize tul LLM loop contract
42c77b0 Handle no-op updates and archive state
86fa990 Restructure tul update runtime boundaries
d79f288 Hotfix tul runtime syntax and newlines
```

Fresh clone checks passed:

```text
python -m py_compile bin/tul
python -m py_compile lib/tulcore/*.py
python scripts/evaluate-entrypoint-strategy.py
```

## Current stage

Stage 2 adoption: **Option 2 — README brief + dedicated handoff**.

This package adopts Option 2 as the production entrypoint strategy and adds an explicit `tul update <project> --latest` / `-l` alias for newest matching package selection from configured inbox roots.

## Known state

- `tul update` is the default full-loop command.
- Compact handoff is the default terminal handoff surface.
- Full protocol output is available through `tul handoff <project> --full`.
- Project instructions are available through `tul instructions` and `tul handoff <project> --instructions`.
- Repeated/already-applied package updates should exit as `noop` instead of attempting an empty commit.
- Entrypoint strategy testing favored Option 2 over README-only or README-heavy strategies.

## Known remaining debt

- Apply safety audit is next: directory copy must be restricted or explicitly gated.
- `tul init` should eventually generate or repair global config and aliases.
- Recovery/debug commands need deeper implementation after the LLM loop surface is stable.
- `humtr/ai` onboarding remains the first major external repo target.
