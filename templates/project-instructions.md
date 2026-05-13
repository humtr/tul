# tul project instructions

You are working with `humtr/tul`, the Terminal Update Loop runtime.

## Start here

1. Read `tul-vf-latest.md` when the user uploads it.
2. Read `README.md`.
3. Read `docs/status/current.md`.
4. Read `docs/manifest.md`.
5. Read `docs/roadmap.md`.
6. Read `docs/commands.md`.
7. Read `docs/package-spec.md` before proposing or producing a package.

Treat only the active read-next documents as current sources of truth. Retired documentation belongs to Git history or historical ledgers unless the user asks for historical context.

## Ownership

```text
README.md                  entrypoint only
docs/status/current.md      current verified state
docs/manifest.md            invariants and ownership map
docs/roadmap.md             future queue
docs/commands.md            command semantics
docs/package-spec.md        package contract
docs/decisions.md           historical rationale
docs/learning-log.md        historical lessons
templates/*                 copy-ready support material
```

## Canonical commands

Use only the canonical command surface:

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
- Remote HEAD verification is part of a successful update when push is enabled.
- Do not use `git add -A` or `git add .` in the normal path.
- Do not force push in the normal path.
- Project policy belongs in `.tul.yml`.
- Environment paths and aliases belong in global config.
- LLM packages should use `tul-package.yml + files/ + README.md`.

## Package output

When producing a package, create one cross-platform zip:

```text
.zip
tul-package.yml
README.md
files/
```

The zip root must contain `tul-package.yml` directly.

## Source separation

Separate user-stated goals, terminal-verified facts, repo-documented facts, assistant interpretation, and unresolved uncertainty.
