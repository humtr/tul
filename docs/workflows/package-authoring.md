# package authoring

Packages are cross-platform zip archives with this root layout:

```text
tul-package.yml
README.md
files/
apply.sh
apply.ps1
```

## Required manifest fields

`tul-package.yml` must include:

```text
name
target.project
target.repo
target.branch
apply.files
commit.files
commit.message
```

`apply.files`, `commit.files`, and payload paths must agree.

## Authoring helpers

```bash
tul package new <name> --message "Commit message"
tul package add <package-dir> <repo-file>...
tul package zip <package-dir>
tul package inspect <package.zip>
tul package check <package.zip>
```

## Application

Normal user application is:

```bash
tul run
```

Do not instruct the user to stage files manually, use broad staging, or force push.
