# setup onboarding

Repository setup is under `setup`. The default behavior is status output only.

## Status

```bash
tul setup
```

Reports tul version, config path, context path, active/default project, platform paths, inbox roots, and optional target repo status.

## Commands

```bash
tul setup init <target>
tul setup install [target]
tul setup use <project>
```

`setup init` registers a project, `setup install` installs or refreshes the launcher, and `setup use` sets the active project context.

## After setup

```bash
tul show
tul run
```
