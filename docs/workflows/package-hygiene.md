# Package inbox hygiene

Package inbox hygiene keeps `tul package latest` focused on current candidate packages without treating shared download folders as tul-owned storage. It is package transport hygiene, not package application, not source export, and not backup management.

## Storage roles

- `/sdcard/Download` is a shared external download folder. Tul may scan it for valid package archives, but unrelated zip files are report-only.
- `/sdcard/termux/import/tul/inbox` is the tul project package inbox. Valid matching tul package archives can be ingested here.
- `/sdcard/termux/import/tul/package-quarantine/...` is for tul-owned package hygiene moves. Files are moved, not deleted.

## Commands

Start with a dry-run:

```bash
tul package hygiene
```

The dry-run separates candidates into three groups:

- valid matching packages outside the project inbox that can be ingested;
- duplicate or invalid archives already inside the project inbox that can be quarantined;
- external invalid archives that are report-only and not selected for movement.

Move valid matching packages from external roots into the project inbox:

```bash
tul package hygiene --ingest
```

After review, quarantine stale project-inbox package archives:

```bash
tul package hygiene --quarantine
```

`--ingest` and `--quarantine` may be combined, but the recommended flow is to run them separately after reviewing the dry-run output.

## Selection policy

K2-fix selects only:

- valid matching tul packages outside the project inbox for ingest;
- invalid archives inside the project inbox for quarantine;
- older duplicate matching packages inside the project inbox for quarantine.

K2-fix does not quarantine invalid archives from shared external roots such as `/sdcard/Download`. Files such as source zips, fonts, NDK archives, subtitles, or other project archives are report-only unless they are valid matching tul packages selected for ingest.

For duplicate matching package groups in the project inbox, the newest package by filesystem mtime is kept by default. Use `--keep-duplicates N` to keep more than one recent duplicate per package name.

## Safety rules

- Default mode is dry-run.
- Shared external invalid archives are never quarantined by default.
- Ingest moves valid matching tul packages into the project inbox.
- Quarantine moves only project-inbox cleanup candidates.
- Files are moved, not deleted.
- Current package selection remains based on configured inbox roots and manifest target matching.
- Work/archive roots remain excluded from package discovery.

## Related commands

```bash
tul package latest
tul package list
tul package hygiene
tul package hygiene --ingest
tul package hygiene --quarantine
```
