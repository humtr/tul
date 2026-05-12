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

Each run writes both timestamped files and stable latest files:

```text
<project>-verify-local-<timestamp>-<head>.md
<project>-verify-local-<timestamp>-<head>.json
<project>-verify-fresh-<timestamp>-<head>.md
<project>-verify-fresh-<timestamp>-<head>.json
<project>-verify-latest.md
<project>-verify-latest.json
```

This reduces long terminal copy/paste. For review, upload the latest markdown artifact instead of pasting the full verify output.

Options:

```bash
tul verify tul --fresh-clone
tul verify tul --fresh-clone --no-log
tul verify tul --fresh-clone --log-dir /sdcard/termux/import/tul/logs/verify
```
