# tul Roadmap

## Current mode

Stage 6 — bounded parallel stabilization, K track.

The J export cleanup track is closed. The current priority is archive/work-state stabilization before returning to manifest, short-term/mid-term/long-term planning, and bounded parallel operations.

## Verified baseline

```text
da00aae271a82473f0958e4e66416a4d6f9d5801
Release gate: PASS
```

## Completed foundations

- Stage 0 — syntax/runtime recovery
- Stage 1 — runtime boundary restructure
- Stage 1.5 — no-op/state cleanup
- Stage 2 — LLM loop contract and README option 2
- Stage 2.1 — launcher/install sync
- Stage 2.1.1 — doctor/no-op output polish
- Stage 2.5 — apply safety audit
- Stage 3 — recovery/debug commands
- Stage 3.1 — recovery state selection
- Stage 4 — init/config onboarding
- Stage 5.1 — verify/fresh clone acceleration
- Stage 5.2 — package discovery polish
- Stage 5.3 — state cleanup UX
- Stage 5.4 — package authoring helper
- Stage 5.5 — package authoring polish
- Stage 6.0 — planning harness insertion
- Stage 6.0.1 — verify artifact logging
- Stage 6.0.2 — short verify artifact names
- Stage 6.1a-f — native context through update-integrated verify gate
- Stage 6.2 — compact verify gate and state output
- Stage 6.4 — package authoring diagnostics
- Stage 6.5 — archive cleanup dry-run guidance
- Stage 6.6 — handoff discoverability
- Stage 6.7 — parallel-readiness gate
- Stage 6.8 — import-root latest verify snapshots
- Stage 6.9 — state verify path alignment

## Recent bundle status

### Closed

- Bundle B — compact gate/state: PASS
- Bundle C — authoring diagnostics: PASS
- Bundle D — archive cleanup dry-run: PASS
- Bundle E — handoff discoverability: PASS
- Bundle F — parallel-readiness gate: PASS
- Bundle G — import-root latest snapshot: PASS
- Bundle H — state verify path alignment: PASS

### Not closed

- Bundle I — repo zip export: verify passed, but source export semantics are unresolved.

Reason: state can show a zip path without proving that the current update generated a fresh, wrapper-free source archive matching the verified HEAD. Full source export also drifted toward backup semantics, which is not the intended role.

## Active bundle

### Bundle J1 — Artifact semantics checkpoint

Status: PASS.

### Bundle J2 — Remove misleading source zip state

Status: PASS.

### Bundle J3 — Review bundle export

Status: PASS.

Goal: implement `tul export review` for compact diff-oriented review bundles.

Expected latest path:

```text
/sdcard/termux/import/tul/tul-review-latest.zip
```

Expected contents: latest verify, state, report, handoff, git facts, changed-files, diff, and changed-file copies.

Acceptance:

- `tul export review` prints PASS and path/sha/size/file counts.
- `/sdcard/termux/import/tul/tul-review-latest.zip` exists.
- The zip contains `tul-vf-latest.md`, `state.json`, `report.md`, `handoff.md`, `changed-files.txt`, and `diff.patch`.
- Review export remains separate from verify and update.

## Next ready queue

### J4 — Review export state/report integration

Goal: make explicit `tul export review` leave evidence in state/report/handoff/latest verify snapshots.

Requirements: state shows `review bundle: <path>` with sha/size/changed-file count, report and handoff include review export evidence, and `tul-vf-latest.md` runtime snapshots refresh after export.

### J5 — Explicit source bundle export

Goal: implement `tul export source` for full source context only when needed.

Requirements: no wrapper directory, root-layout checks, size/file count/sha256, and explicit command invocation.

### Later

- Decide whether successful `tul update` should automatically run review export.
- Windows parity bundle.
- State cleanup policy expansion.
- Docs consistency checks.

## Deferred

Stage X target onboarding, including `humtr/ai`, remains deferred until tul's self-host loop is stable enough to reduce rather than increase bridge work.


## K track — stabilization / cleanup

### K1 — Archive execution safety

Goal: make actual no-op state archive moves safe after a dry-run review.

Acceptance:

- `tul archive --noop --dry-run --keep 3` continues to show inventory, protected references, source dirs, and archive dirs.
- `tul archive --noop --keep 3` moves only older no-op states.
- Latest and latest rollbackable states are protected.
- Non-noop actual moves are refused until separately authorized.
- Successful moves record moved-count evidence in the latest remaining state.

## K2 package inbox hygiene

K2 closes the immediate package-selection hygiene problem. It adds `tul package hygiene` as a dry-run-first command and `tul package hygiene --quarantine` for explicit, reversible movement of invalid archives and older duplicate matching packages.

Acceptance:

- `tul package latest` can point users to hygiene when duplicates or invalid archives exist.
- `tul package hygiene` prints inventory, duplicate groups, selected actions, and quarantine destinations.
- `tul package hygiene --quarantine` moves selected files, not deletes them.
- Incompatible package cleanup remains deferred.
