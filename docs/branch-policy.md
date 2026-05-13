> Historical note: This document predates the Stage 7 command surface redesign. Command examples may use legacy forms. Current canonical commands are `tul show`, `tul package`, `tul update`, `tul verify`, `tul export`, `tul run`, `tul clean`, `tul recover`, and `tul setup`.

# tul Branch Policy

`tul` must treat branch selection as part of the update loop.

The first operational target is `humtr/ai`, and Windows/Termux continuation depends on both environments using the same branch.

---

## 1. Why branch guard exists

Without branch guard, this can happen:

```text
Windows: D:\work\prj\ai on master
Termux:  ~/prj/ai on refactor/stage6-resource-split
LLM:     discussing Stage 6.4 based on refactor/stage6-resource-split
```

The repo may be clean and synced, but the loop is still wrong because it is on the wrong branch.

Therefore `tul` must check the expected branch before mutating commands.

---

## 2. `.tul.yml`

Each repo may define its expected branch:

```yaml
name: ai
repo: humtr/ai
branch: refactor/stage6-resource-split
```

For `humtr/tul` itself:

```yaml
name: tul
repo: humtr/tul
branch: main
```

Supported v0.2 top-level keys:

```text
name
repo
branch
expected_branch
default_branch
```

The v0.2 parser intentionally supports only a tiny top-level subset of YAML.

---

## 3. Command behavior

Read-only/visibility commands show branch warnings but do not fail:

```text
tul status <repo>
tul report <repo>
tul check <repo>
```

Mutating or branch-sensitive commands fail on mismatch:

```text
tul sync <repo>
tul apply <repo>
tul update <repo>
tul publish <repo>
tul rollback <repo>
```

Override exists only for emergency/manual intervention:

```bash
tul update <repo> --allow-branch-mismatch
```

---

## 4. Default workflow

Before Windows/Termux handoff:

```bash
tul update <repo>
```

After switching platform:

```bash
tul sync <repo>
```

If branch mismatch is detected, switch to the expected branch first.

---

## 5. Short-term `humtr/ai` note

If the latest Stage 6 branch should become the stable origin branch, do that deliberately after `tul` branch guard is stable.

Recommended approach:

```text
1. Stabilize tul branch guard.
2. Inspect humtr/ai branches.
3. Decide the single active branch.
4. Merge or fast-forward as needed.
5. Add .tul.yml to humtr/ai with the chosen branch.
6. Use tul sync/update from both Windows and Termux.
```
