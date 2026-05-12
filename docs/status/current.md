# Current status

Latest known version: `0.8.25-stage7-terminology`.

Current mode: Stage 7 terminology hardening after planning consolidation. Stage 6 is closed as the verified stabilization baseline. The first Stage 7 planning consolidation package is applied and verified. The current task is to remove artifact-vocabulary ambiguity before any source-export implementation.

## Verified baseline

Latest verified baseline from the current `tul-vf-latest.md` artifact:

```text
HEAD: 79d27fb07ce52666acb603b714dab33a45079e19
Remote HEAD: 79d27fb07ce52666acb603b714dab33a45079e19
Release gate: PASS
Steps: 25 pass, 0 fail
Working tree: clean
Fresh clone verify: PASS
Latest package: tul-stage7-planning-consolidation-bundle-v1
```

Canonical latest artifact:

```text
/sdcard/termux/import/tul/tul-vf-latest.md
```

When a newer artifact is provided by the user, treat it as the runtime source of truth over this document.

## Closed checkpoints

- Bundle B — compact gate/state: PASS.
- Bundle C — authoring diagnostics: PASS.
- Bundle D — archive cleanup dry-run: PASS.
- Bundle E — handoff discoverability: PASS.
- Bundle F — parallel-readiness gate: PASS.
- Bundle G — import-root latest snapshot: PASS.
- Bundle H — state verify path alignment: PASS.
- Bundle I — source zip export attempt: verify passed, export semantics not closed.
- Bundle J1 — artifact semantics checkpoint: PASS.
- Bundle J2 — remove misleading source zip state: PASS.
- Bundle J3 — explicit review bundle export: PASS.
- Bundle J4 — review export rewrite/state integration: PASS.
- K1 — archive execution safety: PASS.
- K2 — package inbox ingest policy: PASS.
- K3 — Stage 6 stabilization checkpoint: PASS.
- Stage 7 planning consolidation — PASS at `79d27fb07ce52666acb603b714dab33a45079e19`.

## Current artifact vocabulary

- Runtime baseline: the latest `tul-vf-latest.md` evidence for HEAD, Remote HEAD, release gate, working tree, and fresh clone status.
- Review bundle: currently implemented explicit transport artifact from `tul export review`, written as `tul-review-latest.zip`.
- Source context: manually supplied repo contents used for package generation or code-level diagnosis. A GitHub-generated `tul-main.zip` can serve this role after root layout and intended commit are checked.
- Source export: proposed future tul command and artifact. `tul export source` is not implemented in the current CLI.
- Backup/recovery authority: Git remote, commit hashes, and tul rollback state. Zip artifacts are not backup authority.

See `docs/workflows/artifact-semantics.md`, `docs/workflows/source-context-and-export.md`, `docs/workflows/parallel-readiness.md`, and `docs/workflows/stage7-bounded-parallel-planning.md`.

## Current cleanup model

- `tul archive --noop --dry-run --keep 3` is the inspection path.
- `tul archive --noop --keep 3` is the only accepted actual archive move class at this checkpoint.
- `tul package hygiene` reports shared external invalid archives without moving them.
- `tul package hygiene --ingest` moves valid matching tul packages into the project inbox.
- `tul package hygiene --quarantine` only applies to project-inbox cleanup candidates.

## Stage 7 active package

Recommended package:

```text
tul-stage7-terminology-audit-bundle-v1
```

Goal:

```text
Clarify artifact and source vocabulary across docs and code comments before implementing any source-export command.
```

Parallel class: Yellow.

Reason: this package touches coordination docs and artifact vocabulary. It may update documentation and help/docstrings in one commit, but it must not change runtime behavior or add a `tul export source` command.

## Next ready queue

1. Apply the Stage 7 terminology audit package and close it with `tul-vf-latest.md`.
2. If needed, add a source-export spec package that defines root layout, freshness, HEAD provenance, sha256, bytes, file count, and exclusions.
3. Implement `tul export source` only after the spec is accepted and source context remains a repeated bridge cost.
4. Consider docs drift checking if planning/status baselines drift again.
5. Run Windows parity smoke only after several self-host packages remain stable.

## Deferred

Stage X target onboarding, including `humtr/ai`, remains deferred until tul's self-host loop reduces rather than multiplies bridge work.
