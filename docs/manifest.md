# manifest

`tul` is the Terminal Update Loop runtime for applying LLM-generated packages under user control.

## Durable invariants

- User approval remains required before applying generated packages.
- Normal package application must not use `git add -A` or `git add .`.
- Force push is forbidden in normal operation.
- Push is included by default after successful validation and commit.
- Project policy belongs in `.tul.yml`.
- Environment-specific profiles belong under `docs/environments/` when they are repo-relevant; global user aliases and local machine secrets remain outside the repo.
- Zip artifacts are not backup authority.
- Recovery authority is Git remote + commit hash + rollback/recovery state.
- Parallel planning is allowed; update/apply work remains sequential and gated against the latest verified baseline.

## Canonical command surface

```text
tul show
tul package
tul update
tul verify
tul export
tul run
tul clean
tul recover
tul setup
```

Command semantics are owned by `docs/commands.md`.

## Normal user loop

```bash
tul run
```

`run` is the whole user-facing loop. If a compatible package is available, it updates first. If no compatible package is available, it refreshes current artifacts for the current HEAD.

## Active document ownership

Default LLM read-next is limited to:

```text
README.md
docs/status/current.md
docs/manifest.md
docs/roadmap.md
docs/commands.md
docs/package-spec.md
```

Ownership:

| File | Owns |
|---|---|
| `README.md` | entrypoint and artifact summary only |
| `docs/status/current.md` | current verified state only |
| `docs/manifest.md` | durable invariants and ownership map |
| `docs/roadmap.md` | future queue and deferred work only |
| `docs/commands.md` | command grammar and command boundaries |
| `docs/package-spec.md` | package contract and package safety |
| `docs/environments/README.md` | repo-relevant environment profiles and platform-local boundaries |
| `docs/decisions.md` | historical decisions and rationale |
| `docs/learning-log.md` | historical lessons |
| `templates/*` | copy-ready prompts/checklists, not source of truth |

A command name may appear in multiple files for orientation, but the ownership table decides which file carries the authoritative explanation.

## Launcher/bootstrap model

Launcher installation belongs to the canonical `setup` command namespace. Fresh devices should bootstrap with:

```bash
python3 bin/tul setup install
```

There is no legacy top-level `install` command. Platform install scripts must call `setup install`, and launcher diagnostics belong to `lib/tulcore/launcher.py`, not ad-hoc script logic.

## Package contract

The package contract is owned by `docs/package-spec.md`.

The minimum structure is:

```text
tul-package.yml + files/ + README.md
```

## Artifact model

| Artifact | Role |
|---|---|
| Git remote + commit hash | canonical source/recovery authority |
| `tul-vf-<head7>.md` | runtime verification evidence for upload |
| `tul-source-<head7>.zip` | source-context transport artifact for upload |
| `tul-review-<head7>.zip` | current-HEAD changed-file review transport artifact for upload |
| state/report/handoff files | local runtime records |

## Stage status

Stage 7 is closed.

Stage 8 document tree compaction is closed after active ownership consolidation, runtime pointer compaction, obsolete-doc deletion, ownership finalization, and environment-note normalization.


## Review artifact basis

Review export must use current Git HEAD as its manifest head. The latest tul state may be included as context, but it must not make a freshly exported review bundle stale after a manual commit or narrow `git rm` cleanup.

## Human-facing upload inbox

The import root is the manual upload inbox. Root-level upload artifacts are head-tagged only:

```text
tul-source-<head7>.zip
tul-review-<head7>.zip
tul-vf-<head7>.md
```

Root-level `*-latest.*` files are removed after export/verify. Dated logs preserve source, review, verify markdown, and verify JSON history. Verify JSON is not part of the default manual upload set unless explicitly requested.

Shared Download roots are intake-only. A selected valid package from an external shared inbox is moved into the project-owned inbox after it is copied into the work area.

## Verification layering

Regression tests validate code contracts and command reachability. They must not require local transport artifacts to exist before the first export on a freshly synced device. Current source/review artifacts and warnings-none status are final run/export acceptance conditions.
