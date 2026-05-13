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
