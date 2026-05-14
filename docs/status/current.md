# current status

Status: Macro Stage A v8 is in progress via `tul-macro-stage-a-launcher-setup-hygiene-v8`.

Baseline before this package:

```text
HEAD: 5c622640acc3458b946f4e1f09e976807b06d40b
Remote HEAD: 5c622640acc3458b946f4e1f09e976807b06d40b
Latest package: tul-macro-stage-a-head-tag-canonical-v7
Release gate: PASS
CLI runtime smoke: PASS
Regression tests: PASS
Source bundle: current
Review bundle: current
Docs drift: clean
Warnings: none
```

## Objective

Close the launcher/setup hygiene debt exposed by a fresh Termux tablet clone where `tul` was not available on `PATH` after `git pull --ff-only`.

This package makes `tul setup install` the canonical launcher installation path and removes the stale top-level `install` call from platform scripts.

## Launcher policy

```text
Canonical setup command: python3 bin/tul setup install [target]
Installed launcher: ~/bin/tul on POSIX/Termux, ~/bin/tul.cmd on Windows
No legacy top-level install command exists.
```

On POSIX/Termux, `setup install` may idempotently add this line to `~/.profile` so future shells can find `tul`:

```bash
export PATH="$HOME/bin:$PATH"
```

The current shell may still require:

```bash
. ~/.profile && hash -r
```

## Active read-next set

```text
README.md
docs/status/current.md
docs/manifest.md
docs/roadmap.md
docs/commands.md
docs/package-spec.md
```

## Validation after applying

```bash
tul package
tul run
```

Expected result: the final screen says `Decision: PASS`, release gate PASS, CLI runtime smoke PASS, regression tests PASS, source/review current, docs drift clean, warnings none, and head-tagged upload files are printed.
