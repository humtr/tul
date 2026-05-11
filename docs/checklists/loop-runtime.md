# Loop runtime checklist

## Fast check

```bash
tul verify tul
tul update tul -l
tul state tul
```

## Fresh clone check

```bash
tul verify tul --fresh-clone
```

## Package discovery

```bash
tul package latest tul
tul package list tul
tul update tul -l --dry-run
```

## State cleanup

```bash
tul state tul --all --limit 5
tul archive tul --noop --dry-run
tul archive tul --noop --keep 3
tul archive tul --imported --dry-run
```

## Invariants

- `tul update <project>` is the full-loop command.
- Push is default after successful commit.
- `--no-push` and `--no-commit` are exceptions.
- Do not use `git add -A` or `git add .` in the normal update path.
- Do not force push.
- Project policy belongs in `.tul.yml`.
- Environment paths and aliases belong in global config.
