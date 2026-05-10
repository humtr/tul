# tul

`tul` means **Terminal Update Loop**.

`tul` is a local, human-controlled automation toolkit for safely moving AI-generated work across this loop:

```text
LLM / assistant
→ user
→ terminal environment
→ local repo / runtime
→ commit + push
→ report back to LLM / assistant
```

The first operational target is **`humtr/ai`**.

`tul` itself is the tooling and self-hosting repo, but the primary reason for `tul` is to make `humtr/ai` updates fast across Windows, Termux, and LLM-assisted sessions.

The LLM side may be ChatGPT, Codex, Gemini, or another assistant.
The terminal side may be Windows, Termux, WSL, or another local shell environment.

The project started from a Termux workflow, but its scope is broader:

- **Windows `D:\work` track**: Windows Terminal + Codex/Gemini + GitHub + local runtime management.
- **Android / Termux track**: mobile ChatGPT handoff + Termux import/update loop.
- **Shared core**: import, apply, check, sweep, commit, push, rollback, report, and cross-platform continuation.

## Default command model

The default command is:

```bash
tul update <repo>
```

`update` is the full-loop command. It is expected to:

```text
sync precheck
→ import/stage incoming artifact
→ extract/apply
→ check
→ sweep repo-local backups
→ check again
→ stage intended files only
→ staged check
→ commit
→ push
→ verify remote HEAD
→ print rollback instructions
→ generate report
```

Split commands exist for debugging, recovery, and manual intervention:

```text
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

See:

- [`docs/commands.md`](docs/commands.md)
- [`docs/workflows/update-pipeline.md`](docs/workflows/update-pipeline.md)
- [`docs/automation-roadmap.md`](docs/automation-roadmap.md)
- [`docs/windows-dwork-environment.md`](docs/windows-dwork-environment.md)

## Windows intake convention

On Windows, downloaded AI artifacts normally enter through:

```text
D:\work\files\downloads
```

`tul` should stage package-local work under:

```text
D:\work\files\downloads\.tul\work
```

`D:\work\var\tmp` remains available for large scratch work, but it is not the ordinary download handoff path.

## Safety defaults

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

## First-class loop

`tul` treats the human as the explicit approval and execution boundary.

```text
LLM proposes
→ user reviews/chooses
→ terminal applies/verifies
→ tul commits/pushes
→ tul reports
→ LLM reviews next step
```

This keeps the loop flexible across Windows and Termux without relying on ChatGPT web crawling or browser automation.
