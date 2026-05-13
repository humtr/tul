# current status

Status: Stage 7 is closed. Stage 8 document tree compaction 2A is verified, and 2B obsolete-doc deletion is being applied as a narrow git cleanup.

Verified baseline before 2B:

```text
HEAD: b7c2007753bb12eae23c5328b3b8d3be15e2f034
Remote HEAD: b7c2007753bb12eae23c5328b3b8d3be15e2f034
Latest package: tul-doc-tree-compaction-stage2-pointer-compaction-v1
Release gate: PASS
Steps: 33 pass, 0 fail
Fresh clone: PASS
Source bundle: current
Review bundle: current
Docs drift: clean
Warnings: none
```

## Active documentation tree

The active read-next set is:

```text
README.md
docs/status/current.md
docs/manifest.md
docs/roadmap.md
docs/commands.md
docs/package-spec.md
```

Supporting ledgers:

```text
docs/decisions.md
docs/learning-log.md
```

Deferred environment note:

```text
docs/windows-dwork-environment.md
```

Templates retained:

```text
templates/llm-handoff-prompt.md
templates/milestone-checklist.md
templates/project-instructions.md
```

## 2B objective

Remove retired compatibility, workflow, experiment, and harness template files after runtime handoff and verify gates have already stopped requiring them.

This is not a command-surface change. The canonical commands remain:

```text
tul show
tul package
tul update
tul verify
tul export
tul run
tul clean
tul recover
tul setup
```

## Normal loop

```bash
tul run
```

## Next verification

After the 2B deletion commit is pushed:

```bash
tul export
tul verify fresh
tul show handoff
tul show exports
```
