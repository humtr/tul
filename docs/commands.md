# tul commands

Primary loop:

```text
tul init <id|repo|path>
tul sync <project|path>
tul update <project|path>
tul update <project|path> --latest
tul update <project|path> -l
tul update <project|path> --package PATH
tul handoff <project|path>
```

`--latest` / `-l` selects the newest matching package from configured `platform.inbox_roots`. Omitting `--package` already uses the same latest-candidate behavior; the flag exists to make the user's intent explicit and copy-friendly.

`--latest` does not scan work/archive roots by default. Those locations can contain stale or already-applied copies.

Status and visibility:

```text
tul status <project|path>
tul report <project|path>
tul check <project|path>
tul doctor [project|path]
tul state <project|path>
tul instructions [project|path]
```

Recovery/debug commands:

```text
tul import [latest|path]
tul apply <project|path>
tul sweep <project|path>
tul publish <project|path>
tul rollback <project|path> [commit]
tul resume <project|path>
tul archive <project|path>
```

The default workflow remains `tul update <project>` or the explicit latest form `tul update <project> --latest`.
Split commands exist for inspection, recovery, and future resume support; they must not replace the default full loop.

`archive` currently archives the latest local tul work state for a project. It does not delete repo files or rewrite git history.
A repeated/already-applied package update should exit as `noop` instead of attempting an empty commit.
