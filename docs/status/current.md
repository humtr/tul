# current status

Status: Stage 8 document compaction is closed. Stage 9A review/current-HEAD export hardening is closed. Stage 9B regression test harness is closed. Stage 9C structural debt reduction is in corrective fix `tul-stage9c-cli-helper-restore-v1`.

Verified baseline before this package:

```text
HEAD: 1efc472191d58d62772ab5bd87838eaf34e39866
Remote HEAD: 1efc472191d58d62772ab5bd87838eaf34e39866
Latest package: tul-stage9b-regression-test-harness-fix-v1
Release gate: PASS
Regression tests: 9 tests OK
Steps: 33 pass, 0 fail
Fresh clone: PASS
Source bundle: current
Review bundle: current
Docs drift: clean
Warnings: none
```

Current package under review: `tul-stage9c-cli-helper-restore-v1`.

Reason: `tul-stage9c-structural-debt-reduction-v1` extracted CLI parser construction but accidentally removed CLI-local helper functions used by `show`, `export`, `verify`, `clean`, and `recover`. The release gate passed because its checks did not run the new unittest harness; the Stage 9B tests caught the regression. This fix restores those helpers without changing command behavior.

## Active read-next set

```text
README.md
docs/status/current.md
docs/manifest.md
docs/roadmap.md
docs/commands.md
docs/package-spec.md
```

## Current document tree

```text
docs/commands.md
docs/decisions.md
docs/environments/README.md
docs/learning-log.md
docs/manifest.md
docs/package-spec.md
docs/roadmap.md
docs/status/current.md
templates/llm-handoff-prompt.md
templates/milestone-checklist.md
templates/project-instructions.md
```

## Stage 9C objective

Reduce structural debt without changing public behavior:

- move release-gate contract checks out of `lib/tulcore/verify.py` into `lib/tulcore/verify_checks.py`;
- move command registration out of `lib/tulcore/cli.py` into `lib/tulcore/cli_parser.py`;
- add regression tests for source/review export integrity status classification;
- touch `lib/tulcore/state.py` last with a small project-matching helper only.

## Validation

```bash
python3 -m unittest discover -s tests
python3 -m py_compile bin/tul lib/tulcore/*.py
git diff --check
tul export
tul verify fresh
tul show exports
```
