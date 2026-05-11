# tul

`tul` means **Terminal Update Loop**.

`tul` is a local, human-controlled automation toolkit for safely moving AI-generated work across this loop:

```text
LLM / assistant → user → terminal environment → local repo / runtime → commit + push → report back to LLM / assistant
```

The first operational target is **`humtr/ai`**. `tul` itself is the tooling and self-hosting repo, but the primary reason for `tul` is to make `humtr/ai` updates fast across Windows, Termux, and LLM-assisted sessions.

## Start here

For a new LLM, coding agent, or review session, read:

1. [`docs/llm/entrypoint.md`](docs/llm/entrypoint.md)
2. [`docs/status/current.md`](docs/status/current.md)
3. [`docs/roadmap.md`](docs/roadmap.md)
4. [`docs/checklists/loop-runtime.md`](docs/checklists/loop-runtime.md)

Terminal handoffs are compact by default and point to these repo-resident documents.

```bash
tul handoff tul
```

Use full mode only when the receiving LLM needs the protocol inline:

```bash
tul handoff tul --full
```

Print copy-ready project instructions with:

```bash
tul instructions
# or
tul handoff tul --instructions
```

## Default command model

The default loop command is:

```bash
tul update <project>
```

`update` is the full-loop command. It is expected to:

```text
sync precheck
→ import package
→ validate manifest
→ safe apply
→ check
→ sweep repo-local backups
→ verify changed files
→ stage intended files only
→ staged check
→ commit
→ push
→ verify remote HEAD
→ print rollback instructions
→ write report/state/handoff
→ print compact LLM handoff
```

Split commands exist for debugging, recovery, and manual intervention. They must not replace the default full loop.

See:

- [`docs/commands.md`](docs/commands.md)
- [`docs/workflows/update-pipeline.md`](docs/workflows/update-pipeline.md)
- [`docs/llm/commands.md`](docs/llm/commands.md)
- [`docs/protocols/command-grammar.md`](docs/protocols/command-grammar.md)

## Safety defaults

`tul` should reduce repetitive work, not remove human control.

```text
Automate repetition.
Ask before risky execution.
Never delete when moving is safer.
Never use git add -A by default.
Never use git add . by default.
Never force-push by default.
Keep every update resumable and reportable.
```

Important clarification:

```text
`tul update <project>` is explicit update intent.
After a successful commit, it should push by default so another platform can continue from the same remote state.
Use --no-commit or --no-push only for debugging/manual intervention.
```

## Package contract

LLM-generated packages should converge on a single cross-platform zip:

```text
<package>.zip
  tul-package.yml
  files/
    ... repo-relative files ...
  README.md
```

Bootstrap fallback scripts may be included during transition:

```text
apply.sh
apply.ps1
```

Normal operation should use `tul-package.yml`, not arbitrary script execution.

## First-class loop

`tul` treats the human as the explicit approval and execution boundary.

```text
LLM proposes → user reviews/chooses → terminal applies/verifies → tul commits/pushes → tul reports → LLM reviews next step
```

Runtime facts such as commit hash, push result, remote HEAD verification, state path, and rollback command belong in terminal handoff output. Durable planning knowledge belongs in repo documents under `docs/` and `templates/`.
