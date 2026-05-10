# tul Automation Roadmap

`tul` means **Termux Update Loop**.

This document defines the staged automation goals for `tul`: a local, human-controlled update loop for moving ChatGPT-generated artifacts from Android/Termux into one or more git repositories, applying them safely, validating the result, and preparing a report for the next assistant turn.

The first target project is `~/prj/ai`, but `tul` must be designed as a multi-project tool.

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
ChatGPT produces package or instructions
→ user downloads the file
→ tul finds it in /sdcard/Download
→ tul imports it into /sdcard/termux/import/tul
→ tul identifies the target project/update package
→ tul applies it only with user confirmation
→ tul validates the repo
→ tul generates a report
→ user performs manual checks when needed
→ user commits/pushes, optionally with tul assistance later
→ assistant verifies remote state if requested
```

---

## 2. Automation levels

### Level 0 — Manual human bridge

Current baseline before `tul`.

```text
User manually:
- downloads ChatGPT artifact
- moves it to /sdcard/termux/import
- copies it into Termux temp directory
- extracts it
- chmods scripts
- runs installer/patcher
- runs validation commands
- assembles logs
- commits and pushes
- asks assistant to verify GitHub
```

Goal: record this baseline so later automation can be measured.

Status: already practiced during `humtr/ai` Stage 6.4.

---

### Level 1 — Repo-local helper scripts

Purpose: reduce repeated validation and install commands inside each target repo.

Examples already introduced in `humtr/ai`:

```text
scripts/install-termux.sh
README Termux install section
```

Typical commands:

```bash
cd ~/prj/ai
./scripts/install-termux.sh
python -m py_compile lib/*.py
bash -n bin/ai
git diff --check
git diff --stat
```

Automation scope:

```text
- project-specific install
- project-specific validation
- runtime deployment
```

Still manual:

```text
- Download → import handoff
- package extraction
- update state tracking
- report generation
- commit/push
```

Target completion criteria:

```text
- each project can define its own install/deploy command
- no project-specific install logic is hardcoded into tul
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
- include repo, branch, HEAD, status, diff stat, validation summary, active package if any

tul clean:
- move known temporary artifacts out of the repo
- never delete by default

tul inbox / tul import:
- scan allowed source directories
- copy candidate packages into tul-managed import storage
- compute sha256
- detect duplicates
- extract archive into tul-managed directory
- do not execute apply scripts yet
```

Allowed source directories:

```text
/sdcard/Download
/sdcard/termux/import
```

Do not scan all of `/sdcard`.

Target completion criteria:

```text
- user can run `tul report ~/prj/ai | termux-clipboard-set`
- user can run `tul import latest` instead of manual cp/tar/chmod discovery
- no automatic patch execution yet
```

Estimated automation level: **Level 2**.

---

### Level 3 — Import queue, active update state, and multi-project support

Purpose: make update progress explicit and resumable.

`tul` should own a structured queue under:

```text
/sdcard/termux/import/tul/
  inbox/
    packages/
    extracted/
  projects/
    <project-id>/
      active.json
      reports/
      archive/
        applied/
        failed/
        skipped/
  logs/
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
~/prj/ai     → ai
~/prj/board  → board
```

`active.json` example:

```json
{
  "project": "ai",
  "repo_path": "/data/data/com.termux/files/home/prj/ai",
  "package_name": "ai_stage65_run_highlight.tar.gz",
  "sha256": "example",
  "state": "imported",
  "started_at": "2026-05-10T17:10:00+09:00",
  "branch_at_start": "refactor/stage6-resource-split",
  "head_at_start": "200fe79",
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

Multi-project `.tul.yml` example:

```yaml
name: ai
repo: humtr/ai

verify:
  commands:
    - python -m py_compile lib/*.py
    - bash -n bin/ai
    - bash -n scripts/*.sh
    - git diff --check
  forbidden_grep:
    - pattern: ai_registry
      paths:
        - bin
        - lib
        - config
        - README.md

deploy:
  command: ./scripts/install-termux.sh

clean:
  patterns:
    - "*.bak"
    - "*.diff"
    - "README.md.stage*.bak"
    - "lib/*.stage*.bak"
    - "ai_tui_stage*.diff"
```

Target completion criteria:

```text
- `tul update ~/prj/ai` can identify whether there is an active update
- `tul inbox` can import packages without manual movement from Download
- `tul report` can tell the assistant what update is active
- multiple projects can use the same tul installation
```

Estimated automation level: **Level 3**.

---

### Level 4 — Confirmed apply with package manifest

Purpose: let `tul` apply ChatGPT-generated packages safely.

Preferred package format:

```text
package.tar.gz
  tul-package.yml
  apply.sh
  rollback.sh        # optional
  README.md
  files/             # optional
  patches/           # optional
```

`tul-package.yml` example:

```yaml
name: ai-stage65-run-highlight
version: 1
target:
  repo: humtr/ai
  project: ai
  branch: refactor/stage6-resource-split
apply:
  script: apply.sh
verify:
  commands:
    - python -m py_compile lib/*.py
    - bash -n bin/ai
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
2. else find apply*.sh
3. else find install*.sh
4. else find *patch*.py
5. else report "no apply script found"
```

Execution rule:

```text
Never execute automatically by default.
Always show:
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
Target: /data/data/com.termux/files/home/prj/ai
Branch: refactor/stage6-resource-split
Apply: apply.sh

Run this package? [y/N]
```

After apply:

```text
- run verify
- generate report
- preserve logs
- mark active state as applied or failed
```

Target completion criteria:

```text
- `tul update <repo>` can import, select, confirm, apply, verify, report
- manifest packages are preferred
- legacy packages are supported only with clear confirmation
```

Estimated automation level: **Level 4**.

---

### Level 4.5 — Deploy, remote-check, and safe commit assistance

Purpose: automate surrounding tasks while preserving final control.

Commands:

```bash
tul deploy <repo>
tul remote-check <repo>
tul commit <repo> --files <file...> --message "<message>"
```

`tul deploy`:

```text
- read .tul.yml deploy.command
- if not present, detect scripts/install-termux.sh
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
- run verify first unless --no-verify is explicitly provided
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

Estimated automation level: **Level 4.5**.

---

### Level 5 — Watch mode and clipboard handoff

Purpose: reduce user handoff cost further without crawling ChatGPT.

Commands:

```bash
tul watch <repo>
tul paste <repo>
```

`tul watch`:

```text
- periodically scan /sdcard/Download and /sdcard/termux/import
- detect new packages
- import into tul queue
- notify user
- do not apply without confirmation
```

`tul paste`:

```text
- read Android clipboard via termux-clipboard-get if available
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
- large files should still use tar.gz/zip package handoff
```

Target completion criteria:

```text
- user only downloads or copies
- tul handles intake and staging
- user still approves execution
```

Estimated automation level: **Level 5**.

---

### Level 6 — API/backend runner, not ChatGPT web crawling

Purpose: optional future automation for users who want API-based workflows.

Allowed direction:

```text
Termux or local server
→ OpenAI API or another model API
→ package generation
→ tul package import/apply/verify loop
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

Estimated automation level: **Level 6**.

---

## 3. Recommended milestone plan

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
- /sdcard/Download scan
- /sdcard/termux/import/tul storage
- no automatic apply
```

Success criteria:

```text
- `tul status ~/prj/ai` works
- `tul verify ~/prj/ai` works
- `tul report ~/prj/ai` produces assistant-ready report
- `tul import latest` copies and extracts latest package
- no destructive operations by default
```

Target automation level: **2.5 → 3**.

---

### v0.2 — Active update state and confirmed apply

Scope:

```text
- projects/<project-id>/active.json
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
- `tul update ~/prj/ai` can safely process a ChatGPT package
- active update is never overwritten silently
- failed update can be resumed or archived
```

Target automation level: **3.5 → 4**.

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

Success criteria:

```text
- `~/prj/ai/.tul.yml` controls verification and deploy behavior
- other repos can define different behavior
- no ai-specific logic is hardcoded in tul
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
- tul watch <repo>
- tul paste <repo>
- clipboard code block extraction
- import/download polling
- optional termux notification later
```

Success criteria:

```text
- user no longer manually moves files from Download
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
- examples include humtr/ai
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

## 4. What not to automate yet

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

## 5. First target project: humtr/ai

`humtr/ai` should be used as the first real integration target.

Initial `.tul.yml` candidate:

```yaml
name: ai
repo: humtr/ai

verify:
  commands:
    - python -m py_compile lib/*.py
    - bash -n bin/ai
    - bash -n scripts/*.sh
    - git diff --check
  forbidden_grep:
    - pattern: ai_registry
      paths:
        - bin
        - lib
        - config
        - README.md

deploy:
  command: ./scripts/install-termux.sh

clean:
  patterns:
    - "*.bak"
    - "*.diff"
    - "README.md.stage*.bak"
    - "lib/*.stage*.bak"
    - "ai_tui_stage*.diff"
```

Do not make `tul` depend on `humtr/ai`.  
Use `humtr/ai` as an example and regression target.

---

## 6. Assistant handoff contract

`tul report` should produce text that can be pasted directly into ChatGPT.

Required report sections:

```text
Repo:
Project:
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

## 7. Definition of done by milestone

| Milestone | Done means |
|---|---|
| v0.1 | user can inspect, verify, report, clean, and import packages |
| v0.2 | user can run confirmed apply/update and resume active state |
| v0.3 | per-project `.tul.yml` controls verify/deploy/clean |
| v0.4 | user can check remote and commit explicit files safely |
| v0.5 | user can avoid manual Download → import movement and stage clipboard snippets |
| v1.0 | stable multi-project package/update loop with docs, examples, and recovery paths |

---

## 8. Summary

`tul` should aim for **Level 3 in v0.1**, **Level 4 by v0.2/v0.3**, and **Level 5 by v1.0**.

The goal is not full autonomy.  
The goal is a reliable, local, resumable, multi-project update loop where repetitive transport, verification, reporting, and state tracking are automated while risky decisions remain under user control.
