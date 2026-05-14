# roadmap

## Current baseline

Stage 8 document compaction is closed. Stage 9A review/current-HEAD export hardening is closed.

Current stable baseline before this package:

```text
HEAD: 964365e1f425124632ab88fa65736b46c178c238
Release gate: PASS
Source bundle: current
Review bundle: current
Docs drift: clean
Warnings: none
```

## Stage 9B — regression test harness

Active package: `tul-stage9b-regression-test-harness-fix-v1`.

Goal: repair the command-surface test matcher added by `tul-stage9b-regression-test-harness-v1`.

The failed test treated prose inside help descriptions as top-level command entries. The corrected matcher parses argparse's top-level choices from the usage line and checks command-entry lines only.

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
Release gate: PASS
Source bundle: current
Review bundle: current
Docs drift: clean
Warnings: none
```

## Next candidates

### Stage 9C — module decomposition

Only after Stage 9B passes.

Candidate modules:

- `lib/tulcore/cli.py`
- `lib/tulcore/verify.py`
- `lib/tulcore/state.py`

Approach: split one responsibility at a time and keep all Stage 9B tests passing.

### Stage 9D — integration tests

Add side-effecting integration tests for export/package/update behavior after the read-only regression harness is stable.

## Deferred

- safe package-level delete support;
- broader state ledger redesign;
- cross-repo onboarding;
- full Windows profile expansion beyond `docs/environments/README.md`.
