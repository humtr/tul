# Package authoring workflow

Use this workflow when creating a new LLM-generated tul package.

## Fast path

```bash
tul package scaffold tul_example_v1 --target tul --message "Example package"
tul package add tul_example_v1 --target tul README.md docs/roadmap.md
tul package summary tul_example_v1
tul package zip tul_example_v1 --out /sdcard/Download/tul_example_v1.zip --force
tul package check /sdcard/Download/tul_example_v1.zip --target tul
tul update tul -l
```

`package add` copies repo files into `files/` and updates both `apply.files` and `commit.files` in `tul-package.yml`.

## Safety rules

- `package add` is file-only; it refuses directories.
- Directory copy remains manifest-only and should require explicit `allow_directory: true`.
- `package zip` writes `tul-package.yml` at archive root.
- `package check` must pass before update.
- Default application remains `tul update <project> -l` after the package is saved in a configured inbox root.
