# tul Automation Roadmap

`tul` means **Terminal Update Loop**.

This document defines the staged automation goals for `tul`: a local, human-controlled update loop for moving AI-generated artifacts between LLM assistants, users, terminal environments, local repositories, runtimes, and GitHub.

The first operational target is:

```text
humtr/ai
```

The self-hosting/tooling target is:

```text
humtr/tul
```

The core loop is:

```text
LLM / assistant
→ user
→ terminal
→ repo/runtime
→ commit + push
→ report
→ LLM / assistant
```

The LLM may be:

```text
ChatGPT
Codex
Gemini
or another assistant/model interface
```

The terminal may be:

```text
Windows D:\work Terminal
Android Termux
WSL
another local shell
```

The project began as a **Termux Update Loop**, but the intended scope is now broader:

```text
Terminal Update Loop =
  Windows D:\work track
  + Android / Termux track
  + shared safe update/report/apply/publish primitives
```

The first practical targets are:

```text
Windows: D:\work\prj\ai and D:\work\prj\tul
Termux: ~/prj/ai and future Android-side repos
```

---

## 1. Core principle

`tul` should reduce repetitive work, not remove human control.

```text
Automate repetition.
Ask before risky execution.
Never delete when moving is safer.
Never use git add -A by default.
Never force-push by default.
Keep every update resumable and reportable.
```

Important clarification:

```text
`tul update <repo>` is explicit update intent.
After a successful commit, it should push by default so another platform can continue from the same remote state.
Use --no-commit or --no-push only for debugging/manual intervention.
```

The intended loop is:

```text
AI assistant produces package, patch, code block, or instructions
→ user explicitly transfers or approves the artifact
→ tul imports or stages it outside the target repo
→ tul identifies the target project/update package
→ tul applies with user confirmation where needed
→ tul validates the repo
→ tul sweeps local artifacts
→ tul stages intended files only
→ tul commits
→ tul pushes
→ tul verifies remote HEAD
→ tul generates an assistant-ready report
→ user/assistant decide next step
```

`tul` should not depend on one assistant product. It should support work moving fluidly among ChatGPT, Codex, Gemini, local terminal sessions, and GitHub.

---

## 2. Supported environment tracks

### 2.1 Windows `D:\work` track

The Windows track covers the local environment built around:

```text
D:\work\wt\wt.exe
D:\work\wt\wt.ps1
D:\work\wt\D Work Terminal.lnk
D:\work\bin and D:\work\bin\ai
D:\work\home\.codex, .gemini, .ssh
D:\work\tools\runtimes\git, nodejs, python
D:\work\tools\npm-global
D:\work\var\cache, tmp, backup, archive
D:\work\files\downloads
D:\work\prj\
```

Windows-specific automation goals:

```text
- open a reproducible D Work Terminal session
- keep HOME/USERPROFILE under D:\work\home
- keep Codex state under D:\work\home\.codex
- keep Gemini state under D:\work\home\.gemini
- keep SSH config/keys under D:\work\home\.ssh
- keep npm global packages under D:\work\tools\npm-global
- keep npm/pip/XDG caches under D:\work\var\cache
- use D:\work\files\downloads as the ordinary download intake folder
- use D:\work\files\downloads\.tul\work as the default package-local staging area
- keep D:\work\var\tmp available for large scratch or non-download temporary work
- use D:\work\var\backup and D:\work\var\archive for non-destructive moves
- support GitHub SSH over port 443 through D:\work\home\.ssh\config
- support local CA handling through NODE_EXTRA_CA_CERTS when required
- support runtime update helpers for Git, Node.js, and Python
```

The Windows track must treat `D:\work\prj\` as the only normal mutation target during repo work.

It should not modify these paths unless explicitly requested:

```text
D:\work\home
D:\work\wt
D:\work\tools
D:\work\var
D:\work\archive
```

See [`docs/windows-dwork-environment.md`](windows-dwork-environment.md).

### 2.2 Android / Termux track

The Termux track covers the original mobile handoff workflow:

```text
ChatGPT artifact
→ /sdcard/Download
→ /sdcard/termux/import/tul/work
→ ~/prj/
```

Termux-specific automation goals:

```text
- scan only allowed intake directories
- avoid crawling all of /sdcard
- import packages into tul-managed storage
- preserve sha256, source path, and extraction logs
- support termux-clipboard-get / termux-clipboard-set where available
- keep user confirmation before executing generated scripts
- push by default after a successful update so Windows can continue from remote
```

Allowed source directories:

```text
/sdcard/Download
/sdcard/termux/import
```

Do not scan all of `/sdcard`.

---

## 3. Command model

Primary command:

```bash
tul update <repo>
```

`update` is the default full-loop command.

Split/debug/recovery commands:

```bash
tul sync <repo>
tul status <repo>
tul report <repo>
tul import [latest|path]
tul apply <repo>
tul check <repo>
tul sweep <repo>
tul publish <repo>
tul rollback <repo>
```

Naming decisions:

```text
- update = default full-loop command
- sync = platform handoff / remote alignment
- check = verification
- sweep = move artifacts out of repo, not delete
- publish = commit + push + remote verification
- rollback = revert + push
- finish is not used because it is vague
- highway is documentation metaphor only
```

See [`docs/commands.md`](commands.md).

---

## 4. Automation levels

### Level 0 — Manual human bridge

Current baseline before `tul`.

```text
User manually:
- downloads or copies AI output
- moves it to an intake directory
- extracts it
- reviews files
- copies files into a repo
- runs validation commands
- assembles logs
- commits and pushes
- asks assistant to verify remote state
```

Goal: record this baseline so later automation can be measured.

---

### Level 1 — Repo-local helper scripts

Purpose: reduce repeated validation and install commands inside each target repo.

Examples:

```text
scripts/install-termux.sh
README install sections
project-specific verify scripts
D:\work\bin\ai helper commands
```

Target completion criteria:

```text
- each project can define its own install/deploy/check commands
- no project-specific logic is hardcoded into tul
```

---

### Level 2 — Single `tul` CLI for status, sync, check, report, import

Purpose: introduce one command-line entry point and support cross-platform continuation.

Initial command set:

```bash
tul help
tul status <repo>
tul sync <repo>
tul check <repo>
tul report <repo>
tul import latest
```

Expected behavior:

```text
tul status:
- show repo root, branch, HEAD, upstream, dirty/ahead/behind/diverged state

tul sync:
- dirty check
- git fetch
- pull --ff-only when safe
- stop on diverged state

tul check:
- run repo-specific .tul.yml checks if present
- otherwise run safe fallback checks

tul report:
- generate assistant-ready markdown report

tul import:
- scan allowed source directories
- copy candidate packages into tul-managed work root
- compute sha256
- detect duplicates
- extract archives into tul-managed staging
- do not execute apply scripts yet
```

Target completion criteria:

```text
- user can run `tul sync <repo>` when switching Windows/Termux
- user can run `tul report <repo>` and paste the result into an LLM
- no automatic patch execution yet
```

Target automation level: **2 → 3**.

---

### Level 3 — `update` full-loop skeleton

Purpose: make `tul update <repo>` the default command path.

Scope:

```text
- import latest package
- identify target package
- apply with confirmation when needed
- check after apply
- sweep repo-local artifacts
- check before commit
- report
- stop before commit if commit files/message are missing
```

Success criteria:

```text
- `tul update <repo> --no-commit` can run import/apply/check/sweep/report
- `tul update <repo>` stops safely before commit when commit metadata is missing
- split commands exist for debugging but are not the default path
```

Target automation level: **3 → 4**.

---

### Level 4 — `update` commit/push path

Purpose: make `tul update <repo>` complete the cross-platform handoff.

Scope:

```text
- commit metadata from tul-package.yml
- CLI --files/--message fallback
- explicit-file staging only
- staged check
- commit
- push
- fetch
- local HEAD == origin/<branch> verification
- rollback hint
```

Success criteria:

```text
- `tul update <repo> --files ... --message ...` commits and pushes by default
- no `git add -A`
- no force-push
- rollback command is printed
- another platform can immediately `tul sync <repo>` and continue
```

Target automation level: **4 → 4.5**.

---

### Level 5 — Cross-platform package/state stabilization

Purpose: stabilize Windows/Termux continuation.

Scope:

```text
- platform-specific intake/work/archive/backup roots
- active update state
- tul-package.yml package manifest
- publish/rollback split commands
- clipboard/report convenience
```

Success criteria:

```text
- Windows can update and push, Termux can sync and continue
- Termux can update and push, Windows can sync and continue
- active update state can be resumed or archived
- rollback uses revert + push
```

Target automation level: **5**.

---

### Level 6 — API/backend runner, not ChatGPT web crawling

Purpose: optional future automation for API-based workflows.

Allowed direction:

```text
local terminal or backend
→ model API
→ package generation
→ tul package import/apply/check/publish/report loop
```

Avoid:

```text
- scraping ChatGPT web UI
- automating browser sessions to extract ChatGPT output
- storing ChatGPT cookies/tokens
- bypassing rate limits or protection mechanisms
```

---

## 5. What not to automate by default

Do not automate these by default:

```text
- ChatGPT web UI crawling
- git add -A
- force push
- deleting downloaded files
- scanning all of /sdcard
- executing unknown scripts without confirmation
- logging secrets
- storing browser cookies
```

Commit/push is allowed as part of explicit `tul update <repo>` intent.

---

## 6. First target projects

`humtr/ai` should be used as the first real integration target.

`humtr/tul` should be used as the self-hosting documentation and tooling target.

Do not make `tul` depend on `humtr/ai`.
Use `humtr/ai` as an example and regression target.

---

## 7. Assistant handoff contract

`tul report` should produce text that can be pasted directly into an LLM.

Required report sections:

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
Commit:
Push verified:
Rollback:
Manual checks:
Question:
```

For failed updates, include:

```text
Command:
Exit code:
Last output:
Generated files:
Backup paths:
Suggested next action:
```

---

## 8. Definition of done by milestone

| Milestone | Done means |
|---|---|
| v0.1 | user can status/sync/check/report/import |
| v0.2 | `update` can import/apply/check/sweep/report and stop safely |
| v0.3 | `update` supports explicit files/message, staged check, commit |
| v0.4 | `update` pushes by default and verifies remote HEAD |
| v0.5 | Windows/Termux continuation is stable |
| v1.0 | stable multi-project update loop with docs, examples, rollback, and recovery paths |

---

## 9. Summary

`tul` should aim for **a full-loop `update` command**.

The goal is not full autonomy.

The goal is a reliable, local, resumable, multi-platform update loop where:

```text
AI artifact
→ terminal apply/check
→ commit
→ push
→ remote verification
→ LLM report
```

is fast and hard to forget.
