# tul Automation Roadmap

`tul` means **Terminal Update Loop**.

This document defines the staged automation goals for `tul`: a local, human-controlled update loop for moving AI-generated artifacts between ChatGPT/Codex/Gemini, local terminal environments, and one or more GitHub repositories.

The project began as a **Termux Update Loop**, but the intended scope is now broader:

```text
Terminal Update Loop
= Windows D:\work track
+ Android / Termux track
+ shared safe update/report/apply primitives
```

The first practical targets are:

```text
Windows: D:\work\prj\ai and D:\work\prj\tul
Termux:  ~/prj/ai and future Android-side repos
```

---

## 1. Core principle

`tul` should reduce repetitive work, not remove human control.

```text
Automate repetition.
Ask before risky execution.
Never delete when moving is safer.
Never commit or push by default.
Keep every update resumable and reportable.
```

The intended loop is:

```text
AI assistant produces package or instructions
-> user places the artifact in a safe intake area
-> tul imports or stages it outside the target repo
-> tul identifies the target project/update package
-> tul applies only with user confirmation
-> tul validates the repo
-> tul generates an assistant-ready report
-> user performs manual checks when needed
-> user commits/pushes explicitly
-> assistant verifies remote state if requested
```

---

## 2. Supported environment tracks

### 2.1 Windows D:\work track

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
D:\work\prj\<repo>
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
- use D:\work\var\tmp as artifact intake/staging
- use D:\work\var\backup and D:\work\var\archive for non-destructive moves
- support GitHub SSH over port 443 through D:\work\home\.ssh\config
- support local CA handling through NODE_EXTRA_CA_CERTS when required
- support runtime update helpers for Git, Node.js, and Python
```

The Windows track must treat `D:\work\prj\<repo>` as the only normal mutation target during repo work. It should not modify these paths unless explicitly requested:

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
-> /sdcard/Download
-> /sdcard/termux/import
-> ~/prj/<repo>
```

Termux-specific automation goals:

```text
- scan only allowed intake directories
- avoid crawling all of /sdcard
- import packages into tul-managed storage
- preserve sha256, source path, and extraction logs
- support termux-clipboard-get / termux-clipboard-set where available
- keep user confirmation before executing generated scripts
```

Allowed source directories:

```text
/sdcard/Download
/sdcard/termux/import
```

Do not scan all of `/sdcard`.

---

## 3. Automation levels

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

Typical checks:

```bash
git status --short
git diff --check
git diff --stat
python -m py_compile ...
bash -n ...
npm test
```

Automation scope:

```text
- project-specific install
- project-specific validation
- runtime deployment
```

Still manual:

```text
- artifact intake
- package extraction
- update state tracking
- report generation
- commit/push
```

Target completion criteria:

```text
- each project can define its own install/deploy/verify commands
- no project-specific logic is hardcoded into tul
```

---

### Level 2 — Single `tul` CLI for status, verify, report, clean, import

Purpose: introduce one command-line entry point.

Initial command set:

```bash
tul help
tul status <repo>
tul verify <repo>
tul report <repo>
tul clean <repo>
tul inbox
tul import latest
```

Expected behavior:

```text
tul status:
- show repo root
- show branch
- show HEAD
- show upstream status if available
- show git status --short
- show recent commits

tul verify:
- run repo-specific .tul.yml verification if present
- otherwise run safe fallback checks
- show command results clearly
- stop on failure unless --keep-going is explicitly provided later

tul report:
- generate assistant-ready markdown report
- include repo, branch, HEAD, status, diff stat, validation summary, and active package

tul clean:
- move known temporary artifacts out of the repo
- never delete by default

tul inbox / tul import:
- scan allowed source directories
- copy candidate packages into tul-managed import storage
- compute sha256
- detect duplicates
- extract archives into tul-managed staging
- do not execute apply scripts yet
```

Target completion criteria:

```text
- user can run `tul report <repo>` and paste the result into ChatGPT
- user can run `tul import latest` instead of manual cp/tar/zip discovery
- no automatic patch execution yet
```

---

### Level 3 — Import queue, active update state, and multi-project support

Purpose: make update progress explicit and resumable.

Cross-platform state root examples:

```text
Windows: D:\work\var\tul
Termux:  /sdcard/termux/import/tul
```

Suggested state layout:

```text
tul/
  inbox/
  packages/
  extracted/
  projects/
    <project>/
      active.json
      reports/
      logs/
  archive/
    applied/
    failed/
    skipped/
  index.json
```

Project identification:

```text
1. If repo has .tul.yml:name, use that.
2. Else use git remote slug if available.
3. Else use repo directory basename.
4. If ambiguous, append a short hash of repo root path.
```

Example:

```text
D:\work\prj\ai -> ai
~/prj/ai          -> ai
```

`active.json` example:

```json
{
  "project": "ai",
  "repo_path": "D:\\work\\prj\\ai",
  "package_name": "ai_stage65_run_highlight.zip",
  "sha256": "example",
  "state": "imported",
  "started_at": "2026-05-10T17:10:00+09:00",
  "branch_at_start": "main",
  "head_at_start": "example",
  "apply_script": null
}
```

State model v0.1:

```text
imported
extracted
active
applied
verified
failed
archived
```

Important behavior:

```text
- if active update exists, tul must not overwrite it silently
- tul update should offer resume / archive / mark failed / abort
- tul report should include active update state
```

---

### Level 4 — Confirmed apply with package manifest

Purpose: let `tul` apply AI-generated packages safely.

Preferred package format:

```text
package.zip or package.tar.gz
  tul-package.yml
  apply.ps1 or apply.sh
  rollback.ps1 or rollback.sh   # optional
  README.md                     # optional
  files/                        # optional
  patches/                      # optional
```

`tul-package.yml` example:

```yaml
name: ai-stage65-run-highlight
version: 1
target:
  repo: humtr/ai
  project: ai
apply:
  script: apply.ps1
verify:
  commands:
    - git diff --check
    - python -m py_compile lib/*.py
forbidden:
  - pattern: ai_registry
    paths:
      - bin
      - lib
      - config
      - README.md
```

Fallback for legacy packages:

```text
1. use tul-package.yml apply.script if present
2. else find apply*.ps1 / apply*.sh
3. else find install*.ps1 / install*.sh
4. else find *patch*.py
5. else report "no apply script found"
```

Execution rule:

```text
Never execute automatically by default.
```

Always show:

```text
- package name
- sha256
- target repo
- target branch
- apply script
- changed/created files if known
- confirmation prompt
```

Example confirmation:

```text
Package: ai-stage65-run-highlight
Target: D:\work\prj\ai
Branch: main
Apply: apply.ps1

Run this package? [y/N]
```

After apply:

```text
- run verify
- generate report
- preserve logs
- mark active state as applied or failed
```

---

### Level 4.5 — Deploy, remote-check, and safe commit assistance

Purpose: automate surrounding tasks while preserving final control.

Commands:

```bash
tul deploy <repo>
tul remote-check <repo>
tul commit <repo> --files <paths> --message "<message>"
```

`tul deploy`:

```text
- read .tul.yml deploy.command
- show command before execution
- ask for confirmation
```

`tul remote-check`:

```text
- git fetch origin
- show local HEAD
- show upstream HEAD
- show whether local branch is ahead/behind/up-to-date
- show untracked files
- do not push
```

`tul commit`:

```text
- never use git add -A by default
- require explicit --files
- run verify first unless --no-verify is explicitly provided later
- show diff stat
- show untracked warnings
- ask before commit
```

Target completion criteria:

```text
- user no longer manually assembles push status reports
- user can commit known files safely without accidentally committing backups
- pushing remains explicit user action
```

---

### Level 5 — Watch mode and clipboard handoff

Purpose: reduce user handoff cost further without crawling ChatGPT.

Commands:

```bash
tul watch <inbox>
tul paste <repo>
```

`tul watch`:

```text
- periodically scan allowed intake directories
- detect new packages
- import into tul queue
- notify user
- do not apply without confirmation
```

`tul paste`:

```text
- read clipboard when platform support exists
- detect fenced code blocks
- extract file path hints such as ```file:path/to/file
- save to staging area, not directly over repo by default
- show diff/apply instructions
```

Safety notes:

```text
- no ChatGPT UI crawling
- no cookie/session handling
- no automatic execution from clipboard
- large files should still use package handoff
```

---

### Level 6 — API/backend runner, not ChatGPT web crawling

Purpose: optional future automation for users who want API-based workflows.

Allowed direction:

```text
local terminal or backend
-> model API
-> package generation
-> tul package import/apply/verify/report loop
```

Avoid:

```text
- scraping ChatGPT web UI
- automating browser sessions to extract ChatGPT output
- storing ChatGPT cookies/tokens
- bypassing rate limits or protection mechanisms
```

Target completion criteria:

```text
- if model generation is automated, it happens through an API/backend path
- tul remains local package/update orchestrator
- secrets are never logged
```

---

## 4. Recommended milestone plan

### v0.1 — Local status, verification, reporting, and import queue

Scope:

```text
- bin/tul
- status
- verify
- report
- clean
- inbox/import
- basic project id
- platform-aware intake directories
- tul-managed staging
- no automatic apply
```

Success criteria:

```text
- `tul status <repo>` works on Windows and Termux
- `tul verify <repo>` works
- `tul report <repo>` produces assistant-ready markdown
- `tul import latest` copies and extracts latest package
- no destructive operations by default
```

Target automation level: **2.5 -> 3**.

---

### v0.2 — Active update state and confirmed apply

Scope:

```text
- projects/<project>/active.json
- tul update <repo>
- tul resume <repo>
- manifest package support
- legacy apply script detection
- confirmation prompt
- verify after apply
- report after apply
```

Success criteria:

```text
- `tul update <repo>` can safely process an AI-generated package
- active update is never overwritten silently
- failed update can be resumed or archived
```

Target automation level: **3.5 -> 4**.

---

### v0.3 — Project configuration and deployment hooks

Scope:

```text
- .tul.yml support
- custom verify commands
- forbidden grep rules
- clean patterns
- deploy command
- tul deploy <repo>
```

`.tul.yml` candidate:

```yaml
name: ai
repo: humtr/ai
verify:
  commands:
    - git diff --check
deploy:
  command: ./scripts/install-termux.sh
clean:
  patterns:
    - "*.bak"
    - "*.diff"
```

Success criteria:

```text
- `.tul.yml` controls verification and deploy behavior
- different repos can define different behavior
- no project-specific logic is hardcoded in tul
```

Target automation level: **4**.

---

### v0.4 — Remote check and safe commit helper

Scope:

```text
- tul remote-check <repo>
- tul commit <repo> --files ... --message ...
- explicit file list required
- verify before commit
- untracked warnings
```

Success criteria:

```text
- user can check push status without asking assistant
- user can commit only selected files
- backups are not accidentally committed
```

Target automation level: **4.5**.

---

### v0.5 — Watch and clipboard handoff

Scope:

```text
- tul watch <inbox>
- tul paste <repo>
- clipboard code block extraction
- import/download polling
- optional platform notification later
```

Success criteria:

```text
- user no longer manually moves files from downloads into staging
- user can copy small code blocks into clipboard and stage them safely
- tul still asks before applying or executing
```

Target automation level: **5**.

---

### v1.0 — Stable multi-project update loop

Scope:

```text
- package manifest stabilized
- queue/state stable
- report format stable
- rollback hook supported
- .tul.yml stable
- docs complete
- examples include Windows D:\work and Android Termux
```

Success criteria:

```text
- tul can support at least two different local repos
- tul can recover from interrupted update
- tul can generate reliable assistant-ready reports
- user can complete an update with minimal manual shell work
```

Target automation level: **5**.

---

## 5. What not to automate yet

Do not automate these by default:

```text
- ChatGPT web UI crawling
- automatic apply without confirmation
- git add -A
- automatic push
- deleting downloaded files
- scanning all of /sdcard
- executing unknown scripts
- logging secrets
- storing browser cookies
```

These can be considered later only with explicit safeguards:

```text
- tul commit with explicit --files
- tul watch with confirmation
- API/backend integration
```

---

## 6. First target projects

`humtr/ai` should be used as the first real integration target.

`humtr/tul` should be used as the self-hosting documentation and tooling target.

Do not make `tul` depend on `humtr/ai`. Use `humtr/ai` as an example and regression target.

---

## 7. Assistant handoff contract

`tul report` should produce text that can be pasted directly into ChatGPT.

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

This keeps the loop structured and prevents long-context confusion.

---

## 8. Definition of done by milestone

| Milestone | Done means |
|---|---|
| v0.1 | user can inspect, verify, report, clean, and import packages |
| v0.2 | user can run confirmed apply/update and resume active state |
| v0.3 | per-project `.tul.yml` controls verify/deploy/clean |
| v0.4 | user can check remote and commit explicit files safely |
| v0.5 | user can avoid manual download/import movement and stage clipboard snippets |
| v1.0 | stable multi-project package/update loop with docs, examples, and recovery paths |

---

## 9. Summary

`tul` should aim for **Level 3 in v0.1**, **Level 4 by v0.2/v0.3**, and **Level 5 by v1.0**.

The goal is not full autonomy. The goal is a reliable, local, resumable, multi-project update loop where repetitive transport, verification, reporting, and state tracking are automated while risky decisions remain under user control.
