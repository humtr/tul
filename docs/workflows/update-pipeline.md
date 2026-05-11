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
9. `report.py` and `handoff.py` render the human/LLM outputs.

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
