# Stage 7 package gates

## Common gate

- [ ] package zip root contains `tul-package.yml`, `README.md`, `files/`, `apply.sh`, and `apply.ps1`.
- [ ] `apply.files`, `commit.files`, and payload files match.
- [ ] package inspect/check passes.
- [ ] no broad staging.
- [ ] no force push.
- [ ] `python3 -m py_compile bin/tul lib/tulcore/*.py` passes when code changes are included.
- [ ] `git diff --check` passes.
- [ ] `tul verify fresh` passes after application.

## Command-surface changes

- [ ] normal path is `tul run`.
- [ ] stepwise path remains documented only for diagnostics.
- [ ] `export` commands create files only.
- [ ] status/freshness inspection lives under `show`.
- [ ] templates do not instruct users to run removed top-level commands.

## Run finalization

- [ ] `tul run` handles package-present path.
- [ ] `tul run` handles package-absent artifact refresh path.
- [ ] `tul run dry` documents both paths accurately.

## Run smoke gate checks

For command-surface packages, verify the following before claiming closure:

- `tul help` exposes the canonical command surface: show, package, update, verify, export, run, clean, recover, setup.
- Removed top-level commands remain rejected: status, state, report, handoff, instructions, current, projects, doctor, check, sync, publish, import, apply, resume, rollback, archive, sweep, init, install, use, config.
- the removed export-status form remains rejected; use `tul show exports` for diagnostics.
- `tul run dry` documents both paths: package found and package not found.
- `tul run` package-not-found fallback refreshes export and verify artifacts instead of failing only because no package exists.


## Clean / recover / setup UX checks

- `tul clean` must remain plan-only by default.
- `tul clean states run 3` must parse `3` as the keep count.
- `tul recover` must remain plan-only by default.
- `tul recover rollback` must print a safe rollback command rather than silently mutating the repo.
- `tul setup` must remain status-only by default and print explicit next setup commands.
