# tul commands

Primary loop:

```text
tul init <id|repo|path>
tul sync <project|path>
tul update <project|path>
tul handoff <project|path>
```

Status and visibility:

```text
tul status <project|path>
tul report <project|path>
tul check <project|path>
tul doctor [project|path]
tul state <project|path>
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

The default workflow remains `tul update <project>`.
Split commands exist for inspection, recovery, and future resume support; they must not replace the default full loop.
