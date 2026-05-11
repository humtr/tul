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

## Current stage update

Stage 2.1: launcher/install sync hardening.

This package teaches `tul doctor` to detect stale PATH launchers and adds `tul install` to resync the user launcher with repo `bin/tul`. Operational commands should be alias-first and runnable without `cd` when global config is correct.

## Known remaining debt

- Apply safety audit is active: directory copy is explicitly gated and apply-plan logging is being added.
- `tul init` should eventually generate or repair global config and aliases.
- Recovery/debug commands need deeper implementation after the LLM loop surface is stable.
- `humtr/ai` onboarding remains the first major external repo target.


## Stage 2.1.1 — doctor/no-op output fix

This patch makes launcher diagnostics non-recursive so `tul doctor tul` prints
its report and exits cleanly. It also normalizes no-op push verification wording:
no-op updates do not push, so push verification is `not applicable for no-op`
rather than false or unavailable.

## Stage 2.5 — apply safety audit

This stage hardens `lib/tulcore/apply.py` so packages cannot silently perform broad directory writes. The runtime now builds an apply plan before copy, rejects directory copy unless explicitly allowed, and requires every planned destination to appear in manifest `commit.files`.

Expected package/version: `0.4.4-apply-safety`.

## Stage 3 recovery/debug commands

Status: package prepared. Recovery/debug surface includes `tul import`, `tul state --all/--json`, `tul archive --all`, rollback-from-state, and conservative `resume/apply` guidance. Split commands remain recovery/debug tools; default workflow remains `tul update <project>`.


## Recovery state selection update

`tul import <project> --latest` creates a validated/imported state without a commit. That state may become the newest state, but it is not rollbackable. `tul rollback <project>` now skips non-commit states and selects the newest rollbackable state with a commit. `tul state <project>` shows a latest rollbackable state hint when the newest state has no commit.
