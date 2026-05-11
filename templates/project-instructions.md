# tul project instructions

You are working with `humtr/tul`, the Terminal Update Loop runtime.

## Start here

1. Read `README.md`.
2. Read `docs/llm/entrypoint.md`.
3. Read `docs/status/current.md`.
4. Read `docs/roadmap.md`.
5. Read `docs/checklists/loop-runtime.md`.
6. Read `docs/protocols/llm-handoff-protocol.md` when handling a handoff.
7. Read `docs/protocols/command-grammar.md` when interpreting `/tul ...` commands.

## Invariants

- `tul update <project>` is the default full-loop command.
- Push is included by default after successful validation and commit.
- `--no-push` and `--no-commit` are exceptions.
- Remote HEAD verification is part of successful update when push is enabled.
- Do not use `git add -A` or `git add .` in the normal path.
- Do not force push in the normal path.
- Project policy belongs in `.tul.yml`.
- Environment paths and aliases belong in global config.
- LLM packages should use `tul-package.yml + files/ + README.md`.

## Package command guidance

If the user has saved a package into configured inbox roots, prefer:

```bash
tul update <project> --latest
# or
tul update <project> -l
```

Use exact package paths only when needed:

```bash
tul update <project> --package /path/to/package.zip
```

## Source separation

Separate:

- user-stated goals;
- terminal-verified facts;
- repo-documented facts;
- assistant interpretation;
- unresolved uncertainty.

Do not treat raw web preview anomalies as proof of broken files. Use GitHub file/blob view or fresh clone checks for line counts and syntax.

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
