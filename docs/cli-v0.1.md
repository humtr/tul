# tul CLI v0.1

This document describes the first practical CLI implementation.

The purpose is not to finish every future automation feature.
The purpose is to make the current LLM-user-terminal-GitHub loop materially faster.

---

## Added command

```text
bin/tul
```

This is a Python script intended to run on Windows and Termux.

Run from the repo:

```powershell
python .\bin\tul status D:\work\prj\tul
```

```bash
python ./bin/tul status ~/prj/tul
```

Later installation may expose it as:

```bash
tul status .
```

---

## Implemented commands

```text
tul status <repo>
tul sync <repo>
tul check <repo>
tul verify <repo>
tul report <repo>
tul sweep <repo>
tul import [latest|path]
tul apply <repo>
tul publish <repo> --files ... --message ...
tul update <repo> [--package latest] --files ... --message ...
tul rollback <repo> [--commit <commit>]
```

---

## Most useful command immediately

For already-applied changes:

```powershell
python .\bin\tul update D:\work\prj\tul `
  --files README.md docs\automation-roadmap.md docs\commands.md docs\workflows\update-pipeline.md docs\windows-dwork-environment.md templates\milestone-checklist.md `
  --message "Define tul update as full-loop command"
```

This runs:

```text
check
sweep
explicit-file stage
staged check
commit
push
remote verification
report
```

---

## Windows package intake

On Windows:

```text
D:\work\files\downloads
→ D:\work\files\downloads\.tul\work
```

---

## Termux package intake

On Termux:

```text
/sdcard/Download
→ /sdcard/termux/import/tul/work
```

---

## Safety choices

```text
- no git add -A
- no force push
- sweep moves artifacts, not deletes
- rollback uses git revert + push
- update pushes by default when commit succeeds
```
