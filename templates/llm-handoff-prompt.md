# tul LLM handoff prompt

Use this prompt when handing `humtr/tul` to an LLM session for review, package planning, or package writing.

## Evidence order

Use the newest uploaded artifacts in this order:

```text
1. tul-vf-latest.md
2. tul-source-latest.zip
3. tul-review-latest.zip
4. git-files.txt
```

Treat `tul-vf-latest.md`, `tul show`, `tul show handoff`, and `tul show exports` snapshots as runtime facts. Treat repo docs as durable guidance. Do not rely on prior chat memory when uploaded artifacts answer the question.

## Read-next

Read only the compact active set unless the task requires more:

```text
README.md
docs/status/current.md
docs/manifest.md
docs/roadmap.md
docs/commands.md
```

Read `docs/package-spec.md` when producing or reviewing a package. Read `docs/decisions.md` and `docs/learning-log.md` only for design rationale or past lessons.

## Normal user command

```bash
cd ~/prj/tul

tul run
```

`tul run` is the default loop. Split commands are for diagnostics, recovery, or explicit user request.

## Package-writing boundary

Do not produce a package unless the user explicitly asks for one.

When producing a package, provide one cross-platform zip whose root contains:

```text
tul-package.yml
README.md
files/
```

Optional helper scripts may be included, but normal application must be metadata-driven. Do not hide broad staging, force push, deletion, or arbitrary mutation in helper scripts.

## Required task framing

State:

```text
Scope:
Non-goals:
Files changed:
Validation:
Expected result:
Rollback:
```

Keep command behavior, package contract, and artifact authority unchanged unless the user explicitly asks to change them.
