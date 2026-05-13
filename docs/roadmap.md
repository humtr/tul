# roadmap

This file owns future work only. Current verified state belongs in `docs/status/current.md`; durable invariants belong in `docs/manifest.md`.

## Closed

```text
Stage 7: command surface and artifact loop stabilization
Stage 8: active documentation tree compaction
```

Stage 8 closed outcomes:

```text
- active read-next reduced to six documents;
- obsolete compatibility/workflow/experiment/template documents removed;
- source tree reduced to the compact active surface;
- ownership boundaries are explicit in docs/manifest.md;
- no command-surface change introduced;
- no package contract change introduced.
```

## Optional next work

These are candidates, not active work:

```text
1. Review/state model improvement
   - allow manual git rm / delete commits to produce current review evidence;
   - make latest state distinguish package-run commits from manual cleanup commits.

2. Safe package-level delete support
   - design only if deletion needs to re-enter the package mechanism;
   - keep separate from ordinary copy-mode package application.

3. Windows environment note disposition
   - decide whether docs/windows-dwork-environment.md stays in this repo, moves to a platform/environment area, or leaves the tul repo.

4. Broader runtime hardening
   - test harnesses, stale artifact diagnostics, and cross-repo onboarding remain separate stages.
```

## Stop point

If no optional work is selected, the project can stop after `tul verify fresh` passes with:

```text
Release gate: PASS
Read next: six active docs
Docs drift: clean
```
