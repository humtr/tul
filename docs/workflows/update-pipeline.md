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


## Repo zip export

After a successful full `tul update` with commit, push, and fresh verify passing, tul writes a stable repo zip export to the import root:

```text
/sdcard/termux/import/tul/tul-main.zip
```

This export is a convenience pointer for the next package-generation session, not an archival history. It is overwritten on each successful full update. The export excludes Git metadata, Python caches, test caches, build outputs, dependency folders, existing zip files, backup files, and transient roots such as `logs`, `work`, and `archive` if they appear inside the repo.

Repo zip export failure should not retroactively fail a release gate that already passed. Instead, tul records `repo_zip_export.ok: false` in the handoff-ready state so the latest verify markdown can surface the export problem in its runtime snapshot.

## Repo zip export timing

For full updates, repo zip export runs after fresh verify passes and before report, handoff, final state, and runtime snapshot rewrite. This order makes the export visible in all post-update review surfaces.

Expected latest pair after a successful update:

```text
/sdcard/termux/import/tul/tul-vf-latest.md
/sdcard/termux/import/tul/tul-main.zip
```

If export fails, tul records `repo_zip_export.ok=false` with the error type/message and keeps the release gate result unchanged.


## Artifact semantics correction

The previous repo zip export sections describe the intended convenience export, but that capability is not closed. Treat them as historical design pressure, not a finished invariant.

Current corrected rule:

- `verify.py` owns release-gate artifacts only.
- `state.py` owns decision-state summaries only.
- `handoff.py` owns fresh-session orientation only.
- Review/source zip exports should be separate export responsibilities, not hidden inside verify.
- A path in state is insufficient evidence of a valid source export.

Future implementation should split:

```bash
tul export review
```

from:

```bash
tul export source
```

and should only consider automatic post-update review export after the review bundle format is stable.
