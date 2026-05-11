# Recovery/debug workflow

Default work goes through `tul update <project>`. Split commands exist to inspect state, produce safe rollback commands, and recover from interrupted or repeated package runs.

## Import without applying

```bash
tul import tul --latest
```

This command:

1. selects the newest matching package from configured inbox roots,
2. imports it into the work root,
3. validates `tul-package.yml`,
4. builds `apply-plan.json`,
5. writes `state.json`, and
6. does not modify repo files.

Use this when a package should be inspected before full update.

## State inspection

```bash
tul state tul
tul state tul --all
tul state tul --json
```

The latest state is useful for finding report, handoff, apply log, apply plan, commit, push verification, and failure information.

## Archive state

```bash
tul archive tul
tul archive tul --all
```

Archiving moves work state directories to the configured archive root. It does not delete them.

## Rollback command

```bash
tul rollback tul
tul rollback tul <commit>
```

Rollback prints a safe command sequence using `git revert` and `git push origin <branch>`. It does not execute rollback by default.

## Resume/apply stance

`tul resume` and `tul apply` remain conservative. They inspect and suggest safe next commands rather than silently running partial updates.


## Recovery state selection update

`tul import <project> --latest` creates a validated/imported state without a commit. That state may become the newest state, but it is not rollbackable. `tul rollback <project>` now skips non-commit states and selects the newest rollbackable state with a commit. `tul state <project>` shows a latest rollbackable state hint when the newest state has no commit.
