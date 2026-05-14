# current status

Status: Stage 8 document compaction is closed. Stage 9A review/current-HEAD export hardening is closed. Stage 9B regression test harness is the current package.

Verified baseline before this package:

```text
HEAD: c3b4c4b3a23056432f52e28450a42b1f6bc94eea
Remote HEAD: c3b4c4b3a23056432f52e28450a42b1f6bc94eea
Latest package: tul-stage9a-review-current-head-export-v1
Release gate: PASS
Steps: 33 pass, 0 fail
Fresh clone: PASS
Source bundle: current
Review bundle: current
Docs drift: clean
Warnings: none
```

Current package under review: `tul-stage9b-regression-test-harness-v1`.

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

Add a small regression harness before any larger module split.

The harness should protect:

- six-file handoff read-next;
- active required-doc gate;
- README entrypoint terms;
- canonical command surface;
- export namespace boundary;
- source/review current-head export status.

## Validation

```bash
python3 -m unittest discover -s tests
python3 -m py_compile bin/tul lib/tulcore/*.py
git diff --check
tul verify fresh
tul show exports
```
