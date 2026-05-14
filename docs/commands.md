# tul commands

This file owns command grammar and command boundaries.

## Canonical top-level commands

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

There is no legacy alias layer in the current command surface.

## Normal use

```bash
cd ~/prj/tul
tul run
```

`run` is the normal Terminal Update Loop. It applies a package when one is available. If no compatible package is available, it refreshes current verification and transport artifacts.
Use `tul run --json` when the same result must be captured as one machine-readable object; the human run log is carried in the JSON `output` field.

## Optional preflight

```bash
tul package
```

Shows the newest compatible package candidate. It does not apply anything.

## Stepwise use

```bash
tul package
tul update
tul export
tul verify fresh
tul show
```

Use this only when intentionally inspecting or splitting the loop.

## Command boundaries

| Command | Boundary |
|---|---|
| `tul show` | read-only state and diagnostic output |
| `tul package` | package discovery, inspection, validation, and authoring |
| `tul update` | package application, safety checks, commit, push, and remote-HEAD check |
| `tul verify` | quick/local verification by default |
| `tul verify fresh` | fresh clone verification and uploadable verify artifacts |
| `tul export` | file artifact creation only |
| `tul run` | full Terminal Update Loop |
| `tul clean` | cleanup planning by default |
| `tul recover` | recovery planning by default |
| `tul setup` | setup status by default |

## Status and handoff

```bash
tul show
tul show exports
tul show handoff
tul show report
tul show history 5
```

`show` commands are read-only.

`tul show handoff` prints runtime facts and the active read-next list:

```text
README.md
docs/status/current.md
docs/manifest.md
docs/roadmap.md
docs/commands.md
docs/package-spec.md
```

## Export

```bash
tul export
tul export source
tul export review
```

`export` commands create files. Export freshness/status is shown by `tul show exports`.

## Cleanup

```bash
tul clean
tul clean states
tul clean states run
tul clean states run 3
tul clean packages
tul clean packages run
tul clean backups
```

The default `clean` path is plan-only. Use `run` in the clean namespace for guarded moves.

## Recovery

```bash
tul recover
tul recover rollback
tul recover resume
```

Recovery commands print plans or safe commands. They do not silently rewrite history.

`recover apply` and `recover publish` are advanced debug surfaces, not normal workflow commands.

## Setup

```bash
tul setup
tul setup init
tul setup install [target]
tul setup use
```

`setup` without arguments is status-only. Setup subcommands are explicit setup actions.

On a fresh Termux/Unix device where `tul` is not yet on `PATH`, bootstrap from the repo with:

```bash
cd ~/prj/tul
python3 bin/tul setup install
. ~/.profile 2>/dev/null || true
hash -r
tul show exports
```

There is no top-level `tul install` command. Platform install scripts must call `setup install`.
