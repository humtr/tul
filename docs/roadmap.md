# roadmap

## Current baseline

Stage 8 document compaction is closed. Stage 9A review/current-HEAD export hardening is closed.

Current stable baseline before Stage 9B:

```text
HEAD: c3b4c4b3a23056432f52e28450a42b1f6bc94eea
Release gate: PASS
Source bundle: current
Review bundle: current
Docs drift: clean
Warnings: none
```

## Stage 9B — regression test harness

Package: `tul-stage9b-regression-test-harness-v1`

Goal: add a stdlib `unittest` harness before larger technical-debt reduction work.

Scope:

- `tests/test_handoff_contract.py`
- `tests/test_verify_contract.py`
- `tests/test_command_surface.py`
- `tests/test_export_contract.py`
- `tests/helpers.py`

Acceptance:

```bash
python3 -m unittest discover -s tests
python3 -m py_compile bin/tul lib/tulcore/*.py
git diff --check
tul verify fresh
tul show exports
```

Expected result:

```text
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
