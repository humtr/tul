# loop runtime checklist

## Baseline

- [ ] `git rev-parse HEAD` equals `git rev-parse origin/main`.
- [ ] working tree is clean.
- [ ] `python3 -m py_compile bin/tul lib/tulcore/*.py` passes.
- [ ] `git diff --check` passes.
- [ ] `tul verify fresh` reports release gate PASS.
- [ ] fresh clone verification passes.

## Normal loop

- [ ] `tul run dry` explains the planned path.
- [ ] `tul run` applies a compatible package when one exists.
- [ ] `tul run` refreshes artifacts when no compatible package exists.
- [ ] `tul run` leaves `tul-vf-latest.md` current.
- [ ] `tul run` leaves `tul-source-latest.zip` current.
- [ ] `tul run` leaves `tul-review-latest.zip` current.

## Stepwise loop

- [ ] `tul package` shows the newest compatible package candidate.
- [ ] `tul update` applies, commits, pushes, and remote-checks a package.
- [ ] `tul export` creates source and review artifacts.
- [ ] `tul verify fresh` writes latest verification artifacts.
- [ ] `tul show` summarizes the final state.

## Command surface

- [ ] `tul show` works.
- [ ] `tul show exports` works.
- [ ] `tul package` works.
- [ ] `tul verify` works as quick/local verification.
- [ ] `tul clean` is plan-only by default.
- [ ] `tul clean states run 3` treats `3` as keep count, not as a project target.
- [ ] `tul recover` is plan-only by default.
- [ ] `tul recover rollback` prints a command and does not silently mutate the repo.
- [ ] `tul setup` reports setup status.
- [ ] `tul setup` prints explicit setup subcommands and next commands.

## Stage 7 closure

- [ ] command-surface smoke checks appear in `tul verify fresh`.
- [ ] active docs/templates use the canonical Stage 7 commands.
- [ ] historical docs that retain older command examples are marked.
- [ ] `tul show exports` reports source/review artifacts current.
- [ ] docs drift reports clean.
- [ ] the current status and roadmap point to Stage 8 planning after closure.
