# tul

`tul` means **Terminal Update Loop**. It is a local, human-controlled runtime for moving LLM-generated work through this loop:

```text
LLM / assistant -> user -> terminal environment -> local repo/runtime -> commit + push -> verification/export -> LLM review
```

The current operational target is **`humtr/tul`** itself. Future target repositories remain deferred until this self-hosting loop reduces bridge work rather than multiplies it.

## Normal use

For ordinary operation, run one command from the repo:

```bash
cd ~/prj/tul
tul run
```

`tul run` is the normal user loop. It applies a compatible package when one is available; otherwise it refreshes current artifacts for the current HEAD.

Use `tul package` only when you want to inspect the newest compatible package before running the loop. Use `tul update` only when intentionally splitting the loop.

## LLM entrypoint

If you are an LLM, coding agent, or a new session reviewing this repo, start from runtime evidence and then the active documents:

```text
tul-vf-latest.md
README.md
docs/status/current.md
docs/manifest.md
docs/roadmap.md
docs/commands.md
docs/package-spec.md
```

Do not use prior chat context when uploaded artifacts and repo files answer the question. Runtime facts live in `tul-vf-latest.md` and `tul show` snapshots. Repo docs carry durable guidance.

## Artifact model

| Artifact | Role |
|---|---|
| Git remote + commit hash | canonical source/recovery authority |
| `tul-vf-latest.md` | runtime verification evidence |
| `tul-source-latest.zip` | source-context transport artifact |
| `tul-review-latest.zip` | changed-file review transport artifact |
| state/report/handoff files | local runtime records |

Zip artifacts are transport artifacts, not backup authority. Recovery authority is Git remote plus commit hashes and recovery state.

Use this to inspect transport-artifact freshness:

```bash
tul show exports
```

## Document ownership

```text
README.md                  entrypoint and artifact summary only
docs/status/current.md      current verified state
docs/manifest.md            durable invariants and ownership map
docs/roadmap.md             future queue and deferred work
docs/commands.md            command grammar and command boundaries
docs/package-spec.md        package contract and package safety
docs/decisions.md           historical decisions
docs/learning-log.md        historical lessons
```

Templates under `templates/` are copy-ready support material, not sources of truth.

## Verification gate compatibility terms

The release gate expects these terms to remain visible in README:

```text
LLM entrypoint
tul run
tul update
git add -A
tul-package.yml + files/ + README.md
```

Normal package application must not use `git add -A` or `git add .`.
