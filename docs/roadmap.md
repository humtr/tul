# tul roadmap

## Stage 0 — Syntax/runtime recovery

Status: done.

Related commit: `d79f288 Hotfix tul runtime syntax and newlines`.

## Stage 1 — Runtime boundary restructure

Status: done.

Related commit: `86fa990 Restructure tul update runtime boundaries`.

## Stage 1.5 — No-op/state cleanup

Status: done.

Related commit: `42c77b0 Handle no-op updates and archive state`.

## Stage 2 — LLM loop contract

Status: done candidate.

Related commits:

- `de13ecd Stabilize tul LLM loop contract`
- `df84b64 Add LLM entrypoint strategy test`

## Stage 2 adoption — Compact README entrypoint strategy

Status: active.

Goals:

- Adopt Option 2: README brief + durable docs + dedicated handoff.
- Keep README short enough to be a reliable first-contact surface.
- Keep runtime facts in `tul handoff` output.
- Keep mutable planning in `docs/status/current.md`, `docs/roadmap.md`, and `docs/checklists/loop-runtime.md`.
- Add explicit `tul update <project> --latest` / `-l` command syntax for newest matching package selection.

## Stage 2.1 — Launcher/install sync

Status: active.

Goals:

- Detect when PATH `tul` is stale relative to repo `bin/tul`.
- Provide `tul install [project|path]` for user launcher resync.
- Keep operational examples alias-first and `cd`-free.

## Stage 2.1.1 — Doctor/no-op output polish

Status: active.

Goals:

- Ensure `tul doctor tul` exits cleanly without shell-level abort messages.
- Avoid nested launcher subprocess checks in doctor output.
- Represent no-op push verification as not applicable.

## Stage 2.5 — Apply safety audit

Status: active.

Goals:

- Restrict or explicitly gate directory copy.
- Record apply plans before copying.
- Compare apply destinations with manifest `commit.files` before staging.
- Preserve path traversal protections.

Acceptance:

- Directory copy without `allow_directory: true` is rejected before copying.
- Directory copy with `allow_directory: true` still requires every expanded destination in `commit.files`.
- `apply-plan.json` and `apply.log` are recorded in state/report output.

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

## Stage 3 recovery/debug commands

Status: package prepared. Recovery/debug surface includes `tul import`, `tul state --all/--json`, `tul archive --all`, rollback-from-state, and conservative `resume/apply` guidance. Split commands remain recovery/debug tools; default workflow remains `tul update <project>`.


## Recovery state selection update

`tul import <project> --latest` creates a validated/imported state without a commit. That state may become the newest state, but it is not rollbackable. `tul rollback <project>` now skips non-commit states and selects the newest rollbackable state with a commit. `tul state <project>` shows a latest rollbackable state hint when the newest state has no commit.
