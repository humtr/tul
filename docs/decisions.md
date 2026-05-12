# Decisions

This file records accepted planning and design decisions. It is not a full change log; it explains why durable project rules changed.

## ADR-001 — README is compact entrypoint

Status: accepted

Context: README must be readable by new LLM sessions and users without becoming a complete planning ledger.

Decision: README links to the durable planning harness but does not contain the full manifest, strategy, roadmap, learning log, or decision log.

Consequences: Detailed planning lives in `docs/manifest.md`, `docs/strategy.md`, `docs/roadmap.md`, `docs/status/current.md`, `docs/learning-log.md`, and `docs/decisions.md`.

## ADR-002 — Runtime facts belong in handoff/report/state

Status: accepted

Context: Commit hashes, push verification, state paths, and rollback commands are known at runtime, often after a commit is created.

Decision: Runtime facts are printed by terminal handoff/report/state rather than committed into the same implementation commit.

Consequences: Repo docs carry durable contracts; handoff/report/state carry session facts.

## ADR-003 — `humtr/ai` onboarding is Stage X

Status: accepted

Context: `humtr/ai` is the first operational target, but tul's own loop still benefits from acceleration and hardening.

Decision: `/ai` onboarding is deferred to Stage X until tul's self-host loop reduces rather than multiplies bridge work.

Consequences: Current work focuses on tul self-host acceleration, verification, package discovery, state hygiene, native context, and harness portability.

## ADR-004 — `update -l` is preferred over long package paths for normal use

Status: accepted

Context: Repeated package path variables and long absolute paths keep the user in bridge-work mode.

Decision: Normal package application should use configured inbox roots and `tul update <project> -l`.

Consequences: `--package PATH` remains for exact targeting and recovery, but docs should prefer `-l` until native no-arg update is safe.

## ADR-005 — Planning harness separates manifest, strategy, roadmap, status, learning, and decisions

Status: accepted

Context: Stage 6 accelerates feature work and generates new lessons quickly. A single roadmap cannot safely carry vision, medium-term capability planning, short-term ready queue, current state, and decisions.

Decision: The project uses a repo-resident planning harness:

```text
manifest → strategy → roadmap → status → learning log → decisions
```

Consequences: New packages should update the appropriate planning layer, not blindly edit only `docs/roadmap.md`.

## ADR-006 — Native no-arg commands require context conflict guards

Status: accepted

Context: The desired UX is moving from `tul update tul -l` to `tul update`, but active project and current directory can conflict.

Decision: Native context must infer target only when safe. Mutating commands must stop on conflict and present choices. Read-only commands may warn and prefer current-directory context.

Consequences: Native context is split into steps: context storage, read-only inference, mutating inference, package mismatch guidance.

## ADR-007 — Manifest changes require a higher threshold than roadmap changes

Status: accepted

Context: Execution lessons are frequent. If every lesson changes the manifest, the project loses a stable purpose.

Decision: One-off friction goes to learning log and roadmap. Repeated capability pressure goes to strategy. Human authority, safety, or vision changes may change the manifest and should be recorded here.

Consequences: The manifest remains stable but corrigible.

## ADR-008 — Verification output should be file-backed

Status: accepted

Context: `tul verify --fresh-clone` produces long output that is useful but cumbersome to paste into a chat.

Decision: `tul verify` writes markdown and JSON artifacts by default. The terminal output remains visible, but the stable latest artifact can be uploaded for review.

Consequences: The human bridge shifts from log copying to file handoff. This supports the long-term goal of minimizing repetitive bridge labor while preserving inspectability.

## ADR-009 — Verify artifacts use short upload-friendly names

Status: accepted

Context: Verify artifacts replaced long terminal copy/paste, but long common filename prefixes made repeated uploads hard to distinguish in mobile attachment UIs. Stable `latest` filenames are useful for local automation, while unique timestamped filenames are better for uploaded review evidence.

Decision: Generate short timestamped names using `<project>-vf-<mode>-<yymmdd>-<hhmmss>-<head>`, where `mode` is `f` for fresh-clone verification and `l` for local verification. Also generate stable `tul-vf-latest.*` files. This naming decision is now combined with ADR-013, which removes legacy `tul-verify-latest.*` aliases.

Consequences: The user can upload one short, unique markdown artifact without long terminal paste. Stable review automation should use `tul-vf-latest.md/json`.

## ADR-010 — Native context is staged from read-only to mutating commands

Status: accepted

Context: Repeating project names and long flags preserves bridge work. However, changing commands such as `tul update` can damage the wrong repo if active project, current directory, and package manifest disagree.

Decision: Implement native context in stages. First store active context. Then allow no-arg read-only commands and `tul verify fresh`. Only later allow no-arg mutating commands with conflict guards and package-target mismatch guidance.

Consequences: Users get shorter safe commands early, while update/import/rollback defaults remain guarded until the model is proven.


## ADR-011 — No-arg mutating commands require explicit inference banners

Status: accepted

Context: The project is reducing repeated target and package flags. `tul update` is the desired native command, but silent inference would make it harder to audit which project is being changed.

Decision: No-arg mutating commands may infer the project only when context is unambiguous. They must print a target inference banner and must abort when active project and current-directory project conflict.

Consequences: `tul update`, `tul import`, and `tul rollback` can be short in the common case while preserving inspectability and user authority. Package-target mismatch guidance remains the next safety layer.

## ADR-008 — Package mismatch guidance belongs in discovery, not only update failure

Status: accepted

Context: With native `tul update`, users should not manually infer whether a downloaded package targets the active project.

Decision: Package discovery classifies matching, incompatible, and invalid archives. `tul package latest/list` expose the classification, and update failure messages include concrete next commands.

Consequences: Normal package selection remains safe and manifest-driven while reducing user-side file inspection.

## ADR-012 — Normal update includes a post-update fresh verification artifact

Status: accepted

Context: `tul update` already applies, checks, commits, pushes, verifies remote HEAD, reports rollback, and prints handoff. Requiring a separate `tul verify fresh` command after every successful update keeps the user as a log-transport bridge.

Decision: In the normal full-loop path, `tul update` runs a post-update fresh verification gate after publish/no-op handling. It writes the same markdown/json verify artifacts as `tul verify fresh`, prints a compact PASS/FAIL summary, and records artifact paths in report, state, and handoff. Debug paths such as `--no-commit` or `--no-push` do not run the automatic fresh gate because the remote may intentionally not reflect local changes. `--no-verify` remains available as an exception.

Consequences: The default self-host loop becomes one command shorter. The output order preserves user authority: update report first, commit/push/rollback visibility, fresh verification gate second, LLM handoff last.


## ADR-013 — Canonical verify artifact layout

Status: accepted

Context: Verify artifacts replaced long terminal copy/paste, but the verify log root became cluttered when latest files and timestamped run files lived together. The temporary compatibility aliases also created two apparent naming families: `vf` and `verify`.

Decision: Keep exactly one canonical latest markdown file and one canonical latest JSON file at the verify log root: `<project>-vf-latest.md` and `<project>-vf-latest.json`. Move timestamped run artifacts into date folders directly under the verify log root, for example `logs/verify/260512/<project>-vf-f-260512-152110-9dae1b4.md`. Do not continue generating `tul-verify-latest.*` after the layout implementation.

Consequences: The user can upload the stable latest markdown for normal review, while historical runs remain available without cluttering the root directory. The first implementation must acknowledge that a package modifying verify artifact generation cannot make the running update process use the new layout until the next command.

## ADR-014 — Parallel entry requires a normal update smoke after self-modifying update features

Status: accepted

Context: The update-integrated verify gate modifies the update pipeline itself. Its installation required one manual post-install verification because the old process could not use the new pipeline code while still running.

Decision: Before starting larger parallel bundles, run one docs-only smoke package with normal `tul update`. The smoke passes only if commit, push, post-update fresh verify, latest artifact update, and handoff generation all succeed in one command.

Consequences: Parallel work starts from a proven one-command loop rather than from an assumed loop. The smoke package is intentionally docs-only to isolate runtime behavior from unrelated code changes.

## ADR-015 — Default state output is compact; full history is explicit

Status: accepted

Context: Update state files are essential for rollback, diagnosis, and handoff review, but the default state output became too verbose for the normal self-host loop. No-op and imported states can also be newer than the latest rollbackable commit.

Decision: `tul state` defaults to a compact decision view showing the latest state, latest rollbackable commit, key artifacts, cleanup suggestion, and explicit commands for full history. `tul state --all` preserves the long state summaries, and `tul state --json` preserves machine-readable state output.

Consequences: Routine inspection becomes shorter without losing diagnostic depth. Rollbackability remains visible even when the newest state is a no-op, imported, failed, or otherwise non-rollbackable state.
