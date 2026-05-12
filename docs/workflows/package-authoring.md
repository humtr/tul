# Package authoring workflow

Use this workflow when creating a new LLM-generated tul package.

## Fast path

```bash
tul package scaffold tul_example_v1 --target tul --message "Example package"
tul package add tul_example_v1 --target tul README.md docs/roadmap.md
tul package summary tul_example_v1
tul package zip tul_example_v1 --out /sdcard/Download/tul_example_v1.zip --force
tul package check /sdcard/Download/tul_example_v1.zip --target tul
tul package latest
tul update
```

`package add` copies repo files into `files/` and updates both `apply.files` and `commit.files` in `tul-package.yml`.

## Package check expectations

Before distribution, `tul package check` should pass for the final zip:

```bash
tul package check /sdcard/Download/tul_example_v1.zip --target tul
```

The checker validates:

- `tul-package.yml` is at archive root;
- `README.md` is at archive root;
- payload files live under `files/`;
- generated/cache files such as `.git`, `__pycache__`, and `.pyc` are absent;
- every `apply.files[*].from` source exists in the archive payload;
- every `apply.files[*].from` source is under `files/`;
- every `apply.files[*].to` destination is unique;
- `commit.files` exactly matches the repo-relative destinations in `apply.files[*].to`;
- with `--target`, target project/repo/branch matches the current repo and the apply plan can be built.

## Common failure interpretations

### Nested root layout

If the zip contains `some-directory/tul-package.yml` instead of root `tul-package.yml`, rebuild it from inside the package directory:

```bash
cd /path/to/tul_example_v1
tul package zip . --out /sdcard/Download/tul_example_v1.zip --force
```

Or, when using shell zip directly, run zip with `tul-package.yml`, `README.md`, and `files/` as archive-root entries.

### Payload source mismatch

If `payload covers apply sources` fails, check each `apply.files[*].from` entry and ensure the file exists in the zip under `files/`.

### Commit file mismatch

If `apply destinations match commit.files` fails, make `commit.files` exactly match the destination paths from `apply.files[*].to`. Do not use `git add -A` as a workaround.

## Safety rules

- `package add` is file-only; it refuses directories.
- Directory copy remains manifest-only and should require explicit `allow_directory: true`.
- `package zip` writes `tul-package.yml` at archive root.
- `package check` must pass before update.
- Default application is `tul update` after the package is saved in a configured inbox root.
- Split commands such as `tul import` or explicit `tul update tul --package PATH` are for diagnostics and recovery.
