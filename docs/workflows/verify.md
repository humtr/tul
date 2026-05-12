# tul verify workflow

`tul verify` is a development-acceleration command. It reduces repeated manual checks during tul self-hosting.

Default local verification:

```bash
tul verify tul
```

Fresh-clone verification:

```bash
tul verify tul --fresh-clone
tul verify fresh
```

The command checks:

- repo exists
- branch detection
- `git fetch origin <branch>`
- local HEAD and `origin/<branch>`
- working tree clean
- `python -m py_compile bin/tul`
- `python -m py_compile lib/tulcore/*.py`
- `git diff --check`
- required LLM entrypoint/status/roadmap/checklist/protocol documents
- README entrypoint terms

Fresh clones are created under:

```text
~/tmp/tul-verify-fresh/<project>-<timestamp>
```

This command does not replace `tul update`. In the normal loop, `tul update` applies, commits, pushes, runs a post-update fresh verification gate, writes verify artifacts, and prints the handoff. Use standalone `tul verify fresh` after applying a package that changes `verify.py` if the immediate post-update artifact still reflects old bootstrap code.

## Release gate summary

`tul verify` output begins with a compact decision summary:

```text
# tul verify

Release gate: PASS

Project: tul
Repo: ...
Branch: main
HEAD: ...
Remote HEAD: ...
Fresh clone: ...
Steps: 24 pass, 0 fail
```

The full step list remains in the terminal output and in the markdown artifact. The JSON artifact preserves the machine-readable summary.

## Verify artifacts

By default, `tul verify` writes markdown and JSON artifacts in the platform verify log root. On Termux the default location is:

```text
/sdcard/termux/import/tul/logs/verify/
```

Canonical latest files are kept directly under the tul import root so they sit beside `tul-main.zip`:

```text
<project>-vf-latest.md
<project>-vf-latest.json
```

Timestamped run artifacts are stored under YYMMDD date folders directly under the verify log root. There is no `runs/` layer:

```text
<YYMMDD>/<project>-vf-l-<YYMMDD>-<HHMMSS>-<head7>.md
<YYMMDD>/<project>-vf-l-<YYMMDD>-<HHMMSS>-<head7>.json
<YYMMDD>/<project>-vf-f-<YYMMDD>-<HHMMSS>-<head7>.md
<YYMMDD>/<project>-vf-f-<YYMMDD>-<HHMMSS>-<head7>.json
```

Example:

```text
/sdcard/termux/import/tul/tul-vf-latest.md
/sdcard/termux/import/tul/tul-vf-latest.json
/sdcard/termux/import/tul/logs/verify/260512/tul-vf-f-260512-153345-a1dcc39.md
/sdcard/termux/import/tul/logs/verify/260512/tul-vf-f-260512-153345-a1dcc39.json
```

For review, upload `<project>-vf-latest.md` from the tul import root. It includes the release gate, artifact metadata, a compact `tul state` snapshot, and a compact `tul handoff` snapshot. Upload the timestamped markdown artifact only when comparing multiple runs.

Do not use or generate legacy `tul-verify-latest.*` aliases. Artifact metadata should not contain legacy latest paths.

Options:

```bash
tul verify tul --fresh-clone
tul verify tul --fresh-clone --no-log
tul verify tul --fresh-clone --log-dir /sdcard/termux/import/tul/logs/verify
```

## Runtime snapshots

`tul-vf-latest.md` includes a `## Runtime snapshots` section with compact `tul state` and `tul handoff` output. During `tul update`, the verify result is first written before final state/handoff files exist, then the same markdown artifacts are rewritten after the final `handoff-ready` state is recorded. This keeps one upload file sufficient for normal post-update review.


## Compact state path alignment

Compact `tul state` and the `### tul state` snapshot inside `tul-vf-latest.md` should show the import-root latest markdown path. If an older state file stored the former `logs/verify/<project>-vf-latest.md` location during a bootstrap update, compact output normalizes that stale latest pointer for display. Timestamped run artifacts are not normalized; they remain historical evidence under `logs/verify/YYMMDD/`.
