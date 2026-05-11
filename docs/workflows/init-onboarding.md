# Init workflow

`tul init` onboards an existing or cloneable repo into the Terminal Update Loop.

Accepted targets:

```bash
tul init tul
tul init ~/prj/tul
tul init humtr/tul
```

Responsibilities:

1. Resolve the target as alias, path, or GitHub slug.
2. Clone a slug if the repo path does not exist.
3. Fetch and `pull --ff-only` only when the working tree is clean and the branch
   is simply behind.
4. Register or repair the global project alias.
5. Create or fill missing `.tul.yml` fields.
6. Preserve existing config values and create backups before overwriting config
   files.
7. Print an initial-review handoff by default.

Non-goals:

- no branch switching
- no merge/rebase
- no force push
- no deletion of existing config keys
- no automatic package application
