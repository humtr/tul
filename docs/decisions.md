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

## ADR-008 — Verify artifacts use short upload-friendly names

Status: accepted

Context: Verify artifacts replaced long terminal copy/paste, but long common filename prefixes made repeated uploads hard to distinguish in mobile attachment UIs. Stable `latest` filenames are useful for local automation, while unique timestamped filenames are better for uploaded review evidence.

Decision: Generate short timestamped names using `<project>-vf-<mode>-<yymmdd>-<hhmmss>-<head>`, where `mode` is `f` for fresh-clone verification and `l` for local verification. Also generate stable `tul-vf-latest.*` files. Continue writing legacy `tul-verify-latest.*` aliases temporarily for compatibility.

Consequences: The user can upload one short, unique markdown artifact without long terminal paste. Existing notes/scripts using the old latest filename continue working during the transition.
