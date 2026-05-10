# tul Command Model

This document defines the command names and responsibilities for `tul`.

The primary use case is fast, safe updates to `humtr/ai` across Windows, Termux, and LLM-assisted sessions.

---

## 1. Principle

`tul` is not primarily a general documentation tool.

The first operational target is:

```text
humtr/ai
```

The self-hosting/tooling target is:

```text
humtr/tul
```

The default user intent is:

```text
I have an AI-generated update artifact or patch.
Apply it to the target repo.
Verify it.
Commit it.
Push it.
Make it ready for the next terminal/LLM turn.
```

Therefore the default command must complete the loop.

---

## 2. Primary command

```bash
tul update <repo>
```

`update` is the default full-loop command.

It does **not** mean only “git pull latest changes”.

It means:

```text
apply an incoming AI-generated update to the target repo,
verify it,
sweep local artifacts,
commit it,
push it,
verify the remote branch,
and generate a report.
```

Expected default behavior:

```text
sync precheck
→ import/stage package
→ extract
→ apply
→ check after apply
→ sweep repo-local backup artifacts
→ check working tree
→ determine files/message
→ add explicit files only
→ staged check
→ commit
→ push
→ fetch
→ verify local HEAD == origin/<branch>
→ print revert rollback command
→ generate assistant-ready report
```

Push is included by default because Windows/Termux continuation depends on the remote branch.

Options may stop before the end:

```bash
tul update <repo> --no-commit
tul update <repo> --no-push
tul update <repo> --stop-after apply
tul update <repo> --dry-run
```

These options are for debugging, recovery, and manual intervention.

---

## 3. Platform handoff command

```bash
tul sync <repo>
```

`sync` is for entering a repo from another platform.

Examples:

```powershell
Set-Location D:\work\prj\ai
tul sync .
```

```bash
cd ~/prj/ai
tul sync .
```

Expected behavior:

```text
- detect repo root
- check current branch
- check dirty working tree
- git fetch
- pull --ff-only when safe
- report ahead/behind/diverged state
- stop on dirty or diverged state
```

`sync` does not normally push.

Push belongs to `update` and `publish`.

---

## 4. Split/debug/recovery commands

These commands exist for partial execution and recovery.

They are not the default path.

### `tul import [latest|path]`

Bring an incoming artifact into tul-managed staging.

Windows default:

```text
D:\work\files\downloads
→ D:\work\files\downloads\.tul\work
```

Termux default:

```text
/sdcard/Download
→ /sdcard/termux/import/tul/work
```

### `tul apply <repo>`

Apply a staged package to a repo.

Expected behavior:

```text
- read tul-package.yml when present
- otherwise detect apply.ps1/apply.sh/install script/patch script
- show target repo and script
- ask before execution
- write apply logs
```

### `tul check <repo>`

Run repo verification.

Expected behavior:

```text
- git diff --check
- repo-specific .tul.yml verify commands
- forbidden pattern checks when configured
- syntax checks where configured
```

`verify` may exist as an alias, but `check` is the preferred command.

### `tul sweep <repo>`

Move repo-local backup/temp artifacts out of the repo.

It must not delete by default.

Examples:

```text
.tul-*-backup-*
*.stage*.bak
*_stage*.diff
```

Windows destination example:

```text
D:\work\var\backup\tul\<project>\<timestamp>
```

Termux destination example:

```text
~/tmp/tul-backups/<project>/<timestamp>
```

### `tul publish <repo>`

Commit and push already-applied changes.

`publish` is the split command for the commit/push part of `update`.

Expected behavior:

```text
- sweep
- check working tree
- add explicit files only
- staged check
- commit
- push
- fetch
- verify local HEAD == origin/<branch>
- print rollback command
```

`finish` is intentionally not used as a command name because it is vague.

### `tul rollback <repo>`

Revert a pushed `tul update` or `tul publish` commit.

Default rollback must use:

```bash
git revert <commit>
git push origin <branch>
```

Do not use reset/force-push by default.

---

## 5. Visibility commands

### `tul status <repo>`

Human-readable short status.

Expected output:

```text
repo
project
platform
branch
HEAD
upstream
dirty/ahead/behind/diverged
active update state
```

### `tul report <repo>`

LLM-ready structured report.

The report should be pasteable into ChatGPT/Codex/Gemini.

Required sections:

```text
Repo:
Project:
Platform:
Branch:
HEAD:
Upstream:
Status:
Active package:
Validation:
Diff stat:
Untracked files:
Recent commits:
Manual checks:
Question:
```

---

## 6. Naming decisions

| Concept | Command | Decision |
|---|---|---|
| default full loop | `update` | primary command |
| platform remote alignment | `sync` | keep |
| package intake | `import` | use `import`, not `intake` |
| apply package only | `apply` | split/debug command |
| verify/check repo | `check` | primary; `verify` can be alias |
| move artifacts | `sweep` | use instead of `clean` |
| commit + push | `publish` | use instead of `finish` |
| undo pushed commit | `rollback` | revert + push |
| human status | `status` | keep |
| LLM handoff | `report` | keep |
| metaphor | `highway` | documentation metaphor only, not a command |

---

## 7. Self-hosting

`tul` itself can be updated as a target repo:

```bash
tul update tul
```

or by path:

```powershell
tul update D:\work\prj\tul
```

This means:

```text
apply an AI-generated update to the tul repo,
verify it,
commit it,
push it,
and verify remote HEAD.
```

This is different from updating the installed `tul` binary.

A future installer command may be:

```bash
tul install
tul self-update
```
