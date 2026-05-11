# tul command grammar

This document defines the user-facing LLM command grammar and the terminal command forms that support it.

## Terminal package application

Preferred forms:

```bash
tul update <project> --latest
tul update <project> -l
```

These scan configured inbox roots and use the newest matching package by manifest target.

Exact path form:

```bash
tul update <project> --package /path/to/package.zip
```

Default form:

```bash
tul update <project>
```

This also selects the newest matching package when no explicit package path is provided. `--latest` exists to make that behavior explicit in handoff and LLM-generated instructions.

Invalid combination:

```bash
tul update <project> --latest --package /path/to/package.zip
```

Use either exact path or latest discovery, not both.

## LLM-side phrases

- `/tul next <project>` — read repo and propose next package scope.
- `/tul review <project>` — review pushed commit and handoff.
- `/tul package <project>` — generate a cross-platform tul package.
- `/tul roadmap <project>` — update status/roadmap/checklist.
- `/tul verify <project>` — verify repo consistency.
- `/tul init-review <project>` — perform first review after clone/init.
