# Stage 7 command surface redesign

Status: implemented by `tul-stage7-command-surface-redesign-bundle-v1`.

## Canonical top-level commands

`tul` intentionally exposes only these user-facing top-level commands:

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

No legacy alias layer is part of this design. Internal or retired names such as `state`, `status`, `handoff`, `current`, `projects`, `archive`, `rollback`, `apply`, `resume`, `publish`, `init`, `install`, and `use` are folded into the canonical namespaces.

## Default behavior

| Command | No-argument meaning | Writes files or repo state |
|---|---|---:|
| `tul show` | current state, export freshness, next commands | no |
| `tul package` | latest matching package candidate | no |
| `tul update` | apply latest package, commit, push, remote-HEAD check | yes |
| `tul verify` | quick/local verification, stdout-first | no latest artifact by default |
| `tul verify fresh` | fresh clone verification and latest verify artifacts | yes |
| `tul export` | source and review transport artifacts | yes |
| `tul run` | package → update → export → verify fresh → show | yes |
| `tul clean` | cleanup plan only | no |
| `tul recover` | recovery/rollback plan only | no |
| `tul setup` | setup/config/launcher status | no |

## Boundaries

- `update` is not the full loop. It updates the repo.
- `run` is the full loop. It is the normal one-command user workflow.
- `verify` is quick/local by default. `verify fresh` creates the uploadable verification artifact.
- `export` only creates files. Export status lives under `show exports`.
- `clean` and `recover` are read-only by default; explicit `run` under `clean` performs guarded moves.

## Common workflows

```bash
cd ~/prj/tul

tul package
tul run
```

Stepwise workflow:

```bash
tul package
tul update
tul export
tul verify fresh
tul show
```

Review-oriented uploads after `tul run`:

```text
/sdcard/termux/import/tul/tul-vf-latest.md
/sdcard/termux/import/tul/tul-source-latest.zip
/sdcard/termux/import/tul/tul-review-latest.zip
```


## Closure note

The redesign closes at `c274a27e33dd2e13b91daf42e165042cf69b1d9f` after a post-install `tul verify fresh` reports release gate PASS and fresh clone PASS. A first post-update snapshot generated during the installing update can reflect old verify-gate terms; treat that as bootstrap gate drift only when the subsequent installed verify passes.
