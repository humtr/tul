# Package inbox hygiene

Package inbox hygiene keeps `tul package latest` focused on current candidate packages. It is not package application, not source export, and not backup management.

## Problem

Configured inbox roots can accumulate:

- duplicate matching package archives with the same `tul-package.yml` name;
- invalid zip files without a readable root `tul-package.yml`;
- incompatible packages for other projects or branches.

Duplicates and invalid archives do not necessarily break package selection, but they increase warning noise and make it harder for the user and LLM to verify which file will be applied.

## Command

Start with a dry-run:

```bash
tul package hygiene
```

The dry-run prints inventory counts, duplicate groups, invalid archives, and the files that would be moved. It does not move files.

After review, quarantine selected files:

```bash
tul package hygiene --quarantine
```

The command moves selected files under the platform package-quarantine root. It does not delete files.

## Selection policy

K2 selects only:

- invalid archives;
- older duplicate matching packages with the same package name.

K2 does not quarantine incompatible packages by default. Incompatible packages may belong to another project or branch and require a separate policy.

For duplicate matching package groups, the newest package by filesystem mtime is kept by default. Use `--keep-duplicates N` to keep more than one recent duplicate per package name.

## Safety rules

- Default mode is dry-run.
- Actual moves require `--quarantine`.
- Files are moved, not deleted.
- Current package selection remains based on configured inbox roots and manifest target matching.
- Work/archive roots remain excluded from package discovery.

## Related commands

```bash
tul package latest
tul package list
tul package hygiene
tul package hygiene --quarantine
```
