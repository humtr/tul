# tul verify workflow

`tul verify` is a development-acceleration command. It reduces the repeated manual checks used during tul self-hosting.

Default local verification:

```bash
tul verify tul
```

Fresh-clone verification:

```bash
tul verify tul --fresh-clone
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

This command does not replace `tul update`. It verifies the repo after update or before generating the next package.

## Verify artifacts

By default, `tul verify` now writes timestamped markdown and JSON artifacts in the platform log root. On Termux the default location is:

```text
/sdcard/termux/import/tul/logs/verify/
```

Each run writes short timestamped files and stable latest files:

```text
<project>-vf-l-<yymmdd>-<hhmmss>-<head>.md
<project>-vf-l-<yymmdd>-<hhmmss>-<head>.json
<project>-vf-f-<yymmdd>-<hhmmss>-<head>.md
<project>-vf-f-<yymmdd>-<hhmmss>-<head>.json
<project>-vf-latest.md
<project>-vf-latest.json
```

The short names keep the timestamp and commit hash visible in mobile attachment UIs. For review, upload the short timestamped markdown artifact when comparing multiple runs. Upload `<project>-vf-latest.md` when only the newest run matters.

Compatibility aliases are also written for now:

```text
<project>-verify-latest.md
<project>-verify-latest.json
```

These long `latest` aliases are deprecated and exist only to avoid breaking existing notes or scripts during the transition.

Options:

```bash
tul verify tul --fresh-clone
tul verify tul --fresh-clone --no-log
tul verify tul --fresh-clone --log-dir /sdcard/termux/import/tul/logs/verify
```
