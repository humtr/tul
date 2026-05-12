# update pipeline

`tul update <project>` remains the default full-loop command.

Package source selection has two explicit forms:

```bash
tul update <project> --latest
# shorthand
tul update <project> -l

# exact file
tul update <project> --package /path/to/package.zip
```

`--latest` scans configured `platform.inbox_roots` and chooses the newest package whose `tul-package.yml` target matches the project/repo/branch. It does not scan work/archive roots by default.

The runtime boundary is split into policy modules:

1. `precheck.py` resolves whether the repo may be updated.
   - enforce branch guard
   - refuse dirty working tree unless explicit recovery mode is used
   - fetch origin
   - detect ahead/behind/diverged state
   - fast-forward with `pull --ff-only` when safe
2. `package.py` discovers, imports, hashes, and safely extracts the package.
3. `manifest.py` validates `tul-package.yml` target, copy mode, and commit metadata.
4. `apply.py` builds `apply-plan.json`, rejects unsafe directory copy, verifies planned destinations against `commit.files`, then performs safe copy and writes `apply.log`.
5. `checks.py` runs repo-configured checks and forbidden-pattern checks.
6. `sweep.py` moves repo-local tul backup directories out of the repo.
7. `publish.py` owns changed-file allowlist checks, explicit staging, commit, push, remote HEAD verification, rollback hint generation, and no-op detection.
8. `state.py` records phase transitions, failures, no-op outcomes, and archive metadata.
9. `verify.py` runs the post-update fresh verification gate in the normal full-loop path and writes markdown/json artifacts.
10. `report.py` and `handoff.py` render the human/LLM outputs, including verify artifact pointers.

Successful update still requires remote HEAD verification when commit/push is enabled.
`--no-commit` and `--no-push` are recovery/debug exceptions, not the default workflow.

If applying a package produces no repository changes, update must not attempt an empty commit. It should record `outcome: noop`, produce a report/handoff, and exit successfully.

## Apply safety audit

The apply step is intentionally stricter than normal file copying:

- File copy is the default.
- Directory copy requires `allow_directory: true` on the manifest item.
- Every planned destination must be listed in manifest `commit.files`.
- Duplicate destinations are rejected before copying.
- `apply-plan.json` is written before copy so state/report output can point to the exact planned operations.

## Stage 3 recovery/debug commands

Status: package prepared. Recovery/debug surface includes `tul import`, `tul state --all/--json`, `tul archive --all`, rollback-from-state, and conservative `resume/apply` guidance. Split commands remain recovery/debug tools; default workflow remains `tul update <project>`.


## Package discovery visibility

`--latest` uses configured inbox roots only. To inspect the selected package before applying, use:

```bash
tul package latest tul
tul package list tul
tul update tul --latest --dry-run
```

Dry-run imports, validates, and writes `apply-plan.json`, but does not modify repo files.

## Post-update fresh verification

Normal `tul update` now runs a compact post-update fresh verification gate after publish/no-op handling. The terminal output order is:

1. update report, including package, outcome, commit, push verification, rollback, changed files, and checks;
2. compact `VERIFY FRESH` release gate with PASS/FAIL and artifact paths;
3. LLM handoff with report, state, and verify artifact pointers.

The full verification details are written as markdown and JSON artifacts under the platform verify log root. On Termux, the usual upload file is:

```text
/sdcard/termux/import/tul/tul-vf-latest.md
```

`--no-verify` skips the post-update fresh gate. `--no-commit` and `--no-push` are recovery/debug exceptions and do not run the automatic fresh gate because the remote may intentionally not reflect local changes.

## Latest artifact snapshot rewrite

In the normal `tul update` path, the fresh verify gate runs before the final report, handoff, and handoff-ready state are written. After those files exist, tul rewrites the same verify markdown artifacts so `/sdcard/termux/import/tul/tul-vf-latest.md` includes compact `tul state` and `tul handoff` snapshots.


## Export boundary

`tul update` no longer treats full source zip export as a hidden pre-verify side effect. The failed repo zip experiment showed that a source path in state is not enough to prove freshness, root layout, or provenance. Source/review exports now belong to an explicit post-update phase after commit, push, and fresh verification.

The current update order is:

```text
precheck -> import -> validate -> apply -> checks -> sweep -> publish -> verify -> report/state/handoff -> latest snapshot rewrite -> post-update exports -> latest snapshot refresh
```

The post-update export phase runs only after the core update has already produced commit/push/fresh-verify evidence. Export failures are warning-only and must not alter commit, push, rollback, or release-gate facts.

Export work is split by role:

```bash
tul export review   # compact diff-oriented upload bundle
tul export source   # full source-context bundle
tul export status   # warning-only freshness/docs-drift inspection
```

Normal `tul update` runs source/review export automatically after a successful default update. Recovery/debug paths may disable the phase:

```bash
tul update --no-export
tul update --no-source-export
tul update --no-review-export
```

Neither export is backup authority. Recovery remains Git remote + commit hashes + tul rollback state.

## Artifact semantics correction

The previous repo zip export implementation is retired from the default update loop. Treat it as historical design pressure, not a finished invariant.

Current corrected rule:

- `verify.py` owns release-gate artifacts only.
- `state.py` owns decision-state summaries only.
- `handoff.py` owns fresh-session orientation only.
- Review export and source export are separate responsibilities and must not be hidden inside verify.
- A path in state is insufficient evidence of a valid source export.

Current implementation provides explicit review export:

```bash
tul export review
```

Explicit source export exists as both a manual command and a default post-update artifact refresh. The post-update phase is intentionally after the release gate and warning-only. Manual commands remain useful for recovery/debug or when an artifact was intentionally skipped:

```bash
tul export source
tul export review
tul export status
```


## Source export specification

The source-export contract lives in `docs/workflows/source-export-spec.md`. The command is explicit and runnable after the implementation package closes; automatic post-update source export remains a separate Red-class decision.

## Pre-automation export integrity checkpoint

`tul export status` is the warning-only inspection surface for source/review export freshness and small docs drift checks. It may be run manually or captured in verify snapshots. After the post-update export automation package closes, normal `tul update` should leave source/review artifacts current; stale/missing/invalid artifacts remain warnings, not release-gate failures.
