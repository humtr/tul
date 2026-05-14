# roadmap

## Current baseline

Stage 8 document compaction is closed. Stage 9A review/current-HEAD export hardening is closed. Stage 9B regression test harness is closed.

Current stable baseline before this package:

```text
HEAD: 1efc472191d58d62772ab5bd87838eaf34e39866
Release gate: PASS
Regression tests: 9 tests OK
Source bundle: current
Review bundle: current
Docs drift: clean
Warnings: none
```

## Stage 9C — structural debt reduction

Active corrective package: `tul-stage9c-cli-helper-restore-v1`.

Correction target: restore the CLI helper seam removed during parser extraction. Stage 9C is not closed until both the regression harness and the release gate pass.

Goal: make the largest remaining modules easier to change by extracting narrow, behavior-preserving seams under the Stage 9B regression harness.

Scope:

```text
1. verify.py release-gate checks -> lib/tulcore/verify_checks.py
2. show/export status classification -> direct regression tests
3. cli.py command registration -> lib/tulcore/cli_parser.py
4. state.py touched last with a small project-matching helper
```

Non-goals:

```text
- no command surface change
- no package contract change
- no artifact path change
- no state schema change
- no broad cli.py/state.py rewrite
```

Acceptance:

```bash
python3 -m unittest discover -s tests
python3 -m py_compile bin/tul lib/tulcore/*.py
git diff --check
tul export
tul verify fresh
tul show exports
```

Expected result:

```text
unittest: PASS
show/export/handoff commands: PASS
Release gate: PASS
Source bundle: current
Review bundle: current
Docs drift: clean
Warnings: none
```

## Next candidates

### Stage 9D — larger module decomposition

Only after Stage 9C passes. Candidate work:

- split CLI command handlers by command group;
- split verify artifact rendering from verification execution;
- split compact state rendering from state persistence.

### Stage 9E — side-effecting integration tests

Add controlled integration tests for export/package/update behavior after the structural seams are stable.

## Deferred

- safe package-level delete support;
- broader state ledger redesign;
- cross-repo onboarding;
- full Windows profile expansion beyond `docs/environments/README.md`.
