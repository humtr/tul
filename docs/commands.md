# Commands

Native context:

```bash
tul use tul
tul use tul --default
tul current
tul projects
```

Primary loop:

```bash
tul update
```

Explicit forms remain valid and are recommended when context is ambiguous:

```bash
tul update <project>
tul update <project> -l
tul update <project> --latest
```

Package discovery:

```bash
tul package latest
tul package list
tul package inspect /path/to/package.zip
tul update --dry-run
```

Explicit target forms remain valid:

```bash
tul package latest tul
tul package list tul
tul update tul --latest --dry-run
```

Package authoring:

```bash
tul package scaffold NAME --target tul --message "Commit message"
tul package add NAME --target tul FILE [FILE...]
tul package summary NAME
tul package zip NAME --out /sdcard/Download/NAME.zip --force
tul package check /sdcard/Download/NAME.zip --target tul
```

Verification:

```bash
tul verify
tul verify fresh
```

Explicit forms remain valid:

```bash
tul verify tul
tul verify tul fresh
tul verify tul --fresh-clone
```

Recovery/debug:

```bash
tul state
tul state --all --limit 5
tul rollback
tul import
```

Archive still requires an explicit target until its recommendation/dry-run UX is tightened:

```bash
tul archive tul --noop --dry-run
```

Split commands are recovery/debug tools. The default workflow is now native `tul update` when a project can be inferred safely. Use explicit targets when context is ambiguous.

## Native read-only defaults

Stage 6.1b introduces native defaults for read-only commands. After `tul use <project>` or when running inside a configured project repo, these commands may omit the project argument:

```bash
tul status
tul check
tul verify
tul verify fresh
tul state
tul handoff
tul report
tul package latest
tul package list
```

`fresh` is a shorthand for `--fresh-clone`:

```bash
tul verify fresh
tul verify tul fresh
tul verify tul --fresh-clone
```

Resolution order for omitted read-only targets is:

1. explicit target;
2. current configured repo;
3. active project from `tul use`;
4. `default_project`;
5. the only configured project.

If the current directory project differs from the active project, read-only commands warn and use the current directory project. Mutating commands such as `tul update`, `tul import`, and `tul rollback` refuse no-arg execution on conflict and print concrete choices.

## Native mutating defaults

Stage 6.1c introduces guarded defaults for mutating/recovery commands:

```bash
tul update
tul update --dry-run
tul import
tul rollback
```

Resolution is the same as read-only commands, but active/current-directory conflicts abort instead of warning. No-arg `update` means inferred project + newest matching package from configured inbox roots.
