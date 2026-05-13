# tul Milestone Checklist

Use this checklist before closing a milestone.

## Runtime baseline

- [ ] `git rev-parse HEAD` matches `git rev-parse origin/main`.
- [ ] `tul verify fresh` reports release gate PASS.
- [ ] fresh clone verification passes.
- [ ] working tree is clean.
- [ ] `python3 -m py_compile bin/tul lib/tulcore/*.py` passes.
- [ ] `git diff --check` passes.

## Canonical command surface

- [ ] `tul show` works.
- [ ] `tul package` works.
- [ ] `tul update dry` works.
- [ ] `tul verify` works as quick/local verification.
- [ ] `tul verify fresh` writes latest verify artifacts.
- [ ] `tul export` writes source and review artifacts.
- [ ] `tul run dry` works.
- [ ] `tul clean` is plan-only by default.
- [ ] `tul recover` is plan-only by default.
- [ ] `tul setup` reports setup status.

## Normal loop

- [ ] `tul run` applies a package when one is available.
- [ ] `tul run` refreshes artifacts when no package is available.
- [ ] `tul run` leaves source and review bundles current.
- [ ] `tul run` leaves `tul-vf-latest.md` current.

## Artifact model

- [ ] `tul-vf-latest.md` is the runtime verification evidence.
- [ ] `tul-source-latest.zip` is current when source context is needed.
- [ ] `tul-review-latest.zip` is current when changed-file review is needed.
- [ ] `tul show exports` reports warnings none, or warnings are understood.

## Package safety

- [ ] package zip root contains `tul-package.yml`, `README.md`, `files/`, `apply.sh`, and `apply.ps1`.
- [ ] `apply.files`, `commit.files`, and payload files match.
- [ ] normal path does not use `git add -A` or `git add .`.
- [ ] normal path does not force push.

## Documentation

- [ ] README normal path uses `tul run`.
- [ ] active LLM docs use the canonical command surface.
- [ ] templates use `tul run` as the normal application command.
- [ ] historical docs with old commands are clearly marked historical.
