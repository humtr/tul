# Package authoring workflow

`tul` packages are cross-platform archives with this root layout:

```text
<package>.zip
  tul-package.yml
  README.md
  files/
    ...repo-relative files...
```

Use `tul package` helpers before asking `tul update` to apply a package.

## Scaffold

```bash
tul package scaffold tul_example_v1 --target tul --message "Example package"
```

The scaffold creates a package source directory with `tul-package.yml`, `README.md`, and `files/`.
Edit the manifest so `apply.files` and `commit.files` list exact repo-relative paths.

## Zip

```bash
tul package zip tul_example_v1 --out /sdcard/Download/tul_example_v1.zip
```

The zip command writes archive entries at the package root. It excludes generated/cache files such as `__pycache__`, `.pyc`, and `.git`.

## Check

```bash
tul package check /sdcard/Download/tul_example_v1.zip --target tul
```

`check` validates:

- `tul-package.yml` exists at archive root
- `README.md` exists at archive root
- repo payload lives under `files/`
- generated/cache files are absent
- manifest is valid for the target project/repo/branch
- apply plan can be built against the target repo

## Apply

Prefer explicit latest or exact package mode:

```bash
tul package latest tul
tul update tul -l
```

For an exact archive:

```bash
tul update tul --package /sdcard/Download/tul_example_v1.zip
```
