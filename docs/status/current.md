# Current status

Latest known version: `0.8.27-stage7-source-export`.

Current mode: Stage 7 Green/Yellow hardening after terminology audit. Stage 6 is closed as the verified stabilization baseline. Stage 7 planning consolidation is closed. Stage 7 terminology audit is closed. The current task is to accept source-export specification and package-gate templates before any Orange runtime implementation.

## Verified baseline

Latest verified baseline from the current `tul-vf-latest.md` artifact:

```text
HEAD: 7d7b27a4eb81570482ff4d9eaba1dc7c83429272
Remote HEAD: 7d7b27a4eb81570482ff4d9eaba1dc7c83429272
Release gate: PASS
Steps: 25 pass, 0 fail
Working tree: clean
Fresh clone verify: PASS
Latest package: tul-stage7-terminology-audit-bundle-v1
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
- Stage 7 terminology audit — PASS at `7d7b27a4eb81570482ff4d9eaba1dc7c83429272`.

## Current artifact vocabulary

- Runtime baseline: the latest `tul-vf-latest.md` evidence for HEAD, Remote HEAD, release gate, working tree, and fresh clone status.
- Review bundle: currently implemented explicit transport artifact from `tul export review`, written as `tul-review-latest.zip`.
- Source context: manually supplied repo contents used for package generation or code-level diagnosis. A GitHub-generated `tul-main.zip` can serve this role after root layout and intended commit are checked.
- Source export: proposed future tul command and artifact. `tul export source` is not implemented in the current CLI. The accepted spec lives in `docs/workflows/source-export-spec.md` once the Green/Yellow spec package closes.
- Backup/recovery authority: Git remote, commit hashes, and tul rollback state. Zip artifacts are not backup authority.

See `docs/workflows/artifact-semantics.md`, `docs/workflows/source-context-and-export.md`, `docs/workflows/source-export-spec.md`, `docs/checklists/stage7-package-gates.md`, `docs/workflows/parallel-readiness.md`, and `docs/workflows/stage7-bounded-parallel-planning.md`.

## Current cleanup model

- `tul archive --noop --dry-run --keep 3` is the inspection path.
- `tul archive --noop --keep 3` is the only accepted actual archive move class at this checkpoint.
- `tul package hygiene` reports shared external invalid archives without moving them.
- `tul package hygiene --ingest` moves valid matching tul packages into the project inbox.
- `tul package hygiene --quarantine` only applies to project-inbox cleanup candidates.

## Stage 7 active package

Recommended package:

```text
tul-stage7-source-spec-and-gates-bundle-v1
```

Goal:

```text
Accept the source-export specification and make Stage 7 Green/Yellow package gates copy-ready before any runtime implementation.
```

Parallel class: Yellow.

Reason: this package touches coordination docs, artifact semantics, source-export spec text, and gate checklists. It must not add a `tul export source` command or change runtime behavior.

## Next ready queue

1. Apply the Stage 7 source spec and package gates bundle and close it with `tul-vf-latest.md`.
2. If source context remains a repeated bridge cost, implement `tul export source` as an Orange package using the accepted spec.
3. Consider docs drift checking if planning/status baselines drift again.
4. Refine duplicate package name/hash guidance only if inbox clutter returns.
5. Run Windows parity smoke only after several self-host packages remain stable.

## Deferred

Stage X target onboarding, including `humtr/ai`, remains deferred until tul's self-host loop reduces rather than multiplies bridge work.

## Stage 7 explicit source export implementation

Current package target:

- add `tul export source`;
- write `/sdcard/termux/import/tul/tul-source-latest.zip` by default;
- include `source-manifest.json`, `source-file-list.txt`, and `source-file-sha256s.txt`;
- record final SHA256, payload SHA256, size, source file count, root layout, rewrite, and post-replace verification in command output and latest state when available;
- keep automatic post-update source export out of scope.
