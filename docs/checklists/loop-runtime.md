# Loop runtime checklist

Before trusting a package/update cycle:

```bash
tul verify tul
tul package latest tul
tul update tul -l
tul state tul
```

Fresh clone confidence check:

```bash
tul verify tul --fresh-clone
```

Package authoring checks:

```bash
tul package check /sdcard/Download/package.zip --target tul
tul update tul --latest --dry-run
```

Safety invariants:

- `tul update <project>` remains the default full loop.
- Push is included by default after commit.
- `--no-push` and `--no-commit` are exceptions.
- Do not use `git add -A` or `git add .` in the normal path.
- Do not force push.
- Project policy belongs in `.tul.yml`.
- Environment paths and aliases belong in global config.
- Package archive root must contain `tul-package.yml`, `README.md`, and `files/`.
