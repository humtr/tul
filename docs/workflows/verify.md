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

Canonical latest files are kept directly under the verify log root:

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
/sdcard/termux/import/tul/logs/verify/tul-vf-latest.md
/sdcard/termux/import/tul/logs/verify/tul-vf-latest.json
/sdcard/termux/import/tul/logs/verify/260512/tul-vf-f-260512-153345-a1dcc39.md
/sdcard/termux/import/tul/logs/verify/260512/tul-vf-f-260512-153345-a1dcc39.json
```

For review, upload `<project>-vf-latest.md` when only the newest run matters. Upload the timestamped markdown artifact when comparing multiple runs.

Do not use or generate legacy `tul-verify-latest.*` aliases. Artifact metadata should not contain legacy latest paths.

Options:

```bash
tul verify tul --fresh-clone
tul verify tul --fresh-clone --no-log
tul verify tul --fresh-clone --log-dir /sdcard/termux/import/tul/logs/verify
```
