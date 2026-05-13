# tul project instructions

You are working with `humtr/tul`, the Terminal Update Loop runtime.

## Evidence order

Use the latest uploaded artifacts first:

```text
1. tul-vf-latest.md
2. tul-source-latest.zip
3. tul-review-latest.zip
4. git-files.txt
```

Runtime facts from `tul-vf-latest.md`, `tul show`, `tul show handoff`, and `tul show exports` override older prose and prior chat memory.

## Read-next

Start with:

```text
README.md
docs/status/current.md
docs/manifest.md
docs/roadmap.md
docs/commands.md
```

Read `docs/package-spec.md` when package creation or review is requested. Read `docs/decisions.md` and `docs/learning-log.md` only when rationale or lessons are needed.

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
cd ~/prj/tul

tul run
```

`run` applies a compatible package when one is available. If no compatible package is available, it refreshes verification and transport artifacts for the current HEAD.

## Invariants

- User approval remains required before applying generated packages.
- Push is included by default after successful validation and commit.
- `--no-push` and `--no-commit` are exceptions.
- Remote HEAD verification is part of successful update when push is enabled.
- Do not use `git add -A` or `git add .` in the normal path.
- Do not force push in the normal path.
- Project policy belongs in `.tul.yml`.
- Environment paths and aliases belong in global config.
- Package application is sequential and gated against the latest verified baseline.

## Package output boundary

Do not create a package unless the user explicitly asks for one.

When producing a package, create one cross-platform zip:

```text
<package>.zip
  tul-package.yml
  files/
  README.md
```

Optional `apply.sh` and `apply.ps1` files may be included as helpers, but the normal application path is metadata-driven.

## Source separation

Separate user-stated goals, terminal-verified facts, repo-documented facts, assistant interpretation, and unresolved uncertainty. Do not attribute assistant-created frames to the user unless the user explicitly accepts them.
