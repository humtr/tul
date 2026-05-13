# tul project instructions

You are working with `humtr/tul`, the Terminal Update Loop runtime.

## Start here

1. Read `README.md`.
2. Read `docs/llm/entrypoint.md`.
3. Read `docs/status/current.md`.
4. Read `docs/roadmap.md`.
5. Read `docs/checklists/loop-runtime.md`.
6. Read `docs/protocols/llm-handoff-protocol.md` when handling a handoff.
7. Read `docs/protocols/command-grammar.md` when interpreting command syntax.

## Canonical commands

Use only the Stage 7 canonical command surface:

```text
tul show
tul package
tul update
tul verify
tul export
tul run
tul clean
tul recover
tul setup
```

## Normal user path

```bash
tul run
```

`run` applies a compatible package when available. If no compatible package is available, it refreshes verification and transport artifacts for the current HEAD.

## Invariants

- Push is included by default after successful validation and commit.
- `--no-push` and `--no-commit` are exceptions.
- Remote HEAD verification is part of successful update when push is enabled.
- Do not use `git add -A` or `git add .` in the normal path.
- Do not force push in the normal path.
- Project policy belongs in `.tul.yml`.
- Environment paths and aliases belong in global config.
- LLM packages should use `tul-package.yml + files/ + README.md`.

## Package output

When producing a package, create one cross-platform zip:

```text
<package>.zip
  tul-package.yml
  files/
  README.md
  apply.sh
  apply.ps1
```

The zip root must contain `tul-package.yml` directly.

## Source separation

Separate user-stated goals, terminal-verified facts, repo-documented facts, assistant interpretation, and unresolved uncertainty.
