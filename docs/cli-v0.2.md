> Historical note: This document predates the Stage 7 command surface redesign. Command examples may use legacy forms. Current canonical commands are `tul show`, `tul package`, `tul update`, `tul verify`, `tul export`, `tul run`, `tul clean`, `tul recover`, and `tul setup`.

# tul CLI v0.2

This release stabilizes the first CLI by adding branch guard support.

---

## Added

```text
.tul.yml support
expected branch display in status/report
branch mismatch guard for sync/apply/update/publish/rollback
--allow-branch-mismatch emergency override
```

---

## `.tul.yml`

Example:

```yaml
name: tul
repo: humtr/tul
branch: main
```

The v0.2 parser supports a small top-level subset only:

```text
name
repo
branch
expected_branch
default_branch
```

---

## Important behavior

These commands fail on branch mismatch when `.tul.yml` defines an expected branch:

```text
tul sync
tul apply
tul update
tul publish
tul rollback
```

These commands show branch information without failing:

```text
tul status
tul report
tul check
```

---

## Example

```powershell
$Repo = "D:\work\prj\tul"
$Tul = "D:\work\prj\tul\bin\tul"

Set-Location $Repo
python $Tul status $Repo
```

Expected output includes:

```text
expected : main
```
