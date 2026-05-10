# tul Update Pipeline

This document defines the default full-loop behavior for:

```bash
tul update <repo>
```

The goal is to make the LLM-user-terminal-LLM loop fast enough that `humtr/ai` can be edited from Windows and Termux without losing continuity.

---

## 1. Why `update` is full-loop by default

Windows and Termux share work through GitHub remote branches.

If a change is applied and committed locally but not pushed, the other platform cannot continue from it.

Therefore:

```text
For tul's primary workflow, push is part of completion.
```

`update` should push by default after a successful commit and should verify the remote branch.

Use these only for debugging/manual intervention:

```bash
tul update <repo> --no-commit
tul update <repo> --no-push
tul update <repo> --stop-after apply
```

---

## 2. Full pipeline

`tul update <repo>` should eventually perform:

```text
0. sync precheck
1. intake/import
2. extract/stage
3. identify target package
4. apply
5. check after apply
6. sweep repo-local artifacts
7. check before stage
8. determine commit files/message
9. stage explicit files only
10. staged check
11. commit
12. push
13. remote verification
14. rollback hint
15. report
```

---

## 3. Step details

### 0. Sync precheck

Purpose: avoid applying new work on top of an unknown remote state.

Expected checks:

```text
- repo root exists
- branch exists
- remote exists
- git fetch succeeds
- branch is not diverged
- pull --ff-only is possible when local is behind
```

If the working tree is dirty before an update:

```text
- resume active update if tul has one
- otherwise stop and ask for publish/stash/manual resolution
```

### 1. Intake/import

Windows:

```text
D:\work\files\downloads
→ D:\work\files\downloads\.tul\work\<package-id>
```

Termux:

```text
/sdcard/Download
→ /sdcard/termux/import/tul/work/<package-id>
```

Record:

```text
source path
sha256
package id
target repo
branch/head at start
```

### 2. Extract/stage

Extract archives outside the repo.

Do not unpack directly inside:

```text
D:\work\prj\<repo>
~/prj/<repo>
```

### 3. Identify target package

Preferred source:

```text
tul-package.yml
```

Fallback detection:

```text
apply.ps1 / apply.sh
apply*.ps1 / apply*.sh
install*.ps1 / install*.sh
*patch*.py
```

If target repo/branch is uncertain, stop and ask.

### 4. Apply

Before execution, show:

```text
package name
sha256
target repo
current branch
apply script
expected changed files if known
commit message if known
```

Ask before executing generated scripts.

### 5. Check after apply

Run:

```text
git diff --check
repo-specific .tul.yml verify commands
forbidden pattern checks
syntax checks where configured
```

For `humtr/ai`, initial checks may include:

```text
python -m py_compile lib/*.py
bash -n bin/ai
bash -n scripts/*.sh
grep forbidden pattern e.g. ai_registry
git diff --check
```

### 6. Sweep repo-local artifacts

Move repo-local backup/temp artifacts out of the repo.

Do not delete by default.

Examples:

```text
.tul-*-backup-*
*.stage*.bak
*_stage*.diff
```

Windows destination:

```text
D:\work\var\backup\tul\<project>\<timestamp>
```

Termux destination:

```text
~/tmp/tul-backups/<project>/<timestamp>
```

### 7. Check before stage

Run:

```text
git diff --check
git diff --stat
git status --short
```

Ensure unexpected tracked files are not changed.

### 8. Determine commit files/message

Priority:

```text
1. tul-package.yml commit.files and commit.message
2. CLI --files and --message
3. interactive selection
4. stop before commit if metadata is missing
```

Initial implementation may support only 1 and 2.

### 9. Stage explicit files only

Forbidden by default:

```bash
git add -A
git add .
```

Allowed:

```bash
git add -- <explicit files>
```

### 10. Staged check

Run:

```text
git diff --cached --check
git diff --cached --stat
git diff --cached --name-only
```

Abort if staged files differ from allowed files.

### 11. Commit

Rules:

```text
message required
empty commit forbidden
commit hash recorded
```

### 12. Push

Push current branch:

```bash
git push origin <branch>
```

Do not force-push.

### 13. Remote verification

After push:

```bash
git fetch origin <branch>
```

Then verify:

```text
local HEAD == origin/<branch>
```

This is the source of truth for platform continuation.

### 14. Rollback hint

Print:

```bash
git revert <commit>
git push origin <branch>
```

This is the default rollback path.

### 15. Report

Generate a report containing:

```text
Repo:
Project:
Platform:
Branch:
Commit:
Push verified:
Rollback:
Validation:
Changed files:
Package:
Next platform handoff:
```

---

## 4. Platform continuation examples

### Windows to Termux

Windows:

```powershell
Set-Location D:\work\prj\ai
tul sync .
tul update . --files lib\ai_tui.py --message "Update TUI handling"
```

Termux:

```bash
cd ~/prj/ai
tul sync .
```

### Termux to Windows

Termux:

```bash
cd ~/prj/ai
tul sync .
tul update . --files lib/ai_tui.py --message "Update TUI handling"
```

Windows:

```powershell
Set-Location D:\work\prj\ai
tul sync .
```

---

## 5. Split commands

Split commands are recovery/debug tools.

They should match the pipeline phases:

```text
tul import
tul apply
tul check
tul sweep
tul publish
tul rollback
```

`publish` is the second half of `update`:

```text
sweep → check → stage → staged check → commit → push → remote verification
```

---

## 6. Definition of done

An update is done only when:

```text
- files were applied
- checks passed
- repo-local artifacts were swept
- intended files were staged
- staged checks passed
- commit succeeded
- push succeeded
- local HEAD equals origin/<branch>
- rollback command was printed
- report was generated
```
