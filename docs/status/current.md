# current status

Status: Stage 8 document compaction is closed. Stage 9A review/current-HEAD export hardening is closed. Stage 9B regression test harness is active and this package fixes the command-surface test matcher.

Verified baseline before this package:

```text
HEAD: 964365e1f425124632ab88fa65736b46c178c238
Remote HEAD: 964365e1f425124632ab88fa65736b46c178c238
Latest package: tul-stage9b-regression-test-harness-v1
Release gate: PASS
Steps: 33 pass, 0 fail
Fresh clone: PASS
Source bundle: current
Review bundle: current
Docs drift: clean
Warnings: none
```

Current package under review: `tul-stage9b-regression-test-harness-fix-v1`.

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

## Stage 9B objective

Maintain a small regression harness before any larger module split.

This fix narrows `tests/test_command_surface.py` so it checks argparse top-level choices and command-entry lines, not arbitrary prose in command descriptions. The word `apply` may legitimately appear in the `update` description without being a top-level command.

## Validation

```bash
python3 -m unittest discover -s tests
python3 -m py_compile bin/tul lib/tulcore/*.py
git diff --check
tul export
tul verify fresh
tul show exports
```
