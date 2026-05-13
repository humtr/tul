# tul milestone checklist

Use this checklist before closing a milestone.

## Runtime baseline

- [ ] `git rev-parse HEAD` matches `git rev-parse origin/main`.
- [ ] Working tree is clean before applying the next package.
- [ ] `tul verify fresh` reports release gate PASS after applying the package.
- [ ] Fresh clone verification passes.
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
- [ ] `tul-review-latest.zip` is current when changed-file review is needed, or a stale warning is explicitly understood.
- [ ] `tul show exports` reports current artifacts or known warning boundaries.

## Package safety

- [ ] Package zip root contains `tul-package.yml`, `README.md`, and `files/`.
- [ ] `apply.files`, `commit.files`, and payload files match.
- [ ] No normal path uses `git add -A` or `git add .`.
- [ ] No normal path force-pushes.
- [ ] Deletion, if any, is explicit and narrow; it is not hidden in helper scripts.

## Documentation ownership

- [ ] README is entrypoint only.
- [ ] Current status is owned by `docs/status/current.md`.
- [ ] Invariants and ownership map are owned by `docs/manifest.md`.
- [ ] Future queue is owned by `docs/roadmap.md`.
- [ ] Command semantics are owned by `docs/commands.md`.
- [ ] Package structure is owned by `docs/package-spec.md`.
- [ ] Rationale and lessons are preserved in `docs/decisions.md` and `docs/learning-log.md`.
- [ ] Retired compatibility docs are absent from the active tree or treated only as Git history.
