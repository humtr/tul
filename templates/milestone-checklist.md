# tul milestone checklist

Use this checklist before closing a milestone.

## Runtime baseline

- [ ] `git rev-parse HEAD` matches `git rev-parse origin/main`.
- [ ] working tree is clean before applying the next package.
- [ ] `tul verify fresh` reports release gate PASS after applying the package.
- [ ] fresh clone verification passes.
- [ ] `python3 -m py_compile bin/tul lib/tulcore/*.py` passes when code is present.
- [ ] `git diff --check` passes.

## Canonical command surface

- [ ] `tul show` is read-only state/diagnostic output.
- [ ] `tul package` discovers, inspects, validates, and authors packages.
- [ ] `tul update` applies one compatible package and stages only manifest-declared files.
- [ ] `tul verify` remains quick/local by default.
- [ ] `tul verify fresh` writes latest verify artifacts.
- [ ] `tul export` creates file artifacts only.
- [ ] `tul run` remains the normal user loop.
- [ ] `tul clean` is plan-only by default.
- [ ] `tul recover` is plan-only by default.
- [ ] `tul setup` reports setup status by default.

## Artifact model

- [ ] `tul-vf-latest.md` is current runtime verification evidence.
- [ ] `tul-source-latest.zip` is current when source context is needed.
- [ ] `tul-review-latest.zip` is current when changed-file review is needed.
- [ ] `tul show exports` reports current artifacts or warnings are understood.

## Package safety

- [ ] package zip root contains `tul-package.yml`, `README.md`, and `files/`.
- [ ] `apply.files`, `commit.files`, and payload files match.
- [ ] no normal path uses `git add -A` or `git add .`.
- [ ] no normal path force-pushes.
- [ ] deletion, if any, is explicitly represented and validated; it is not hidden in helper scripts.

## Documentation compaction

- [ ] README read-next points to the compact active doc set.
- [ ] current status is owned by `docs/status/current.md`.
- [ ] invariants are owned by `docs/manifest.md`.
- [ ] command semantics are owned by `docs/commands.md`.
- [ ] package structure is owned by `docs/package-spec.md`.
- [ ] future queue is owned by `docs/roadmap.md`.
- [ ] rationale and lessons are preserved in `docs/decisions.md` and `docs/learning-log.md`.
- [ ] compatibility docs are marked non-canonical if they remain for runtime pointer compatibility.
