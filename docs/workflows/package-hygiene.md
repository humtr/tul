# Package cleanup workflow

Package cleanup keeps shared download folders from polluting package selection without treating unrelated zip files as tul-owned files.

## Roles

```text
/sdcard/Download
  Shared external download area. Scanable, but not tul-owned.

/sdcard/termux/import
  Shared import area. Scanable, but not always tul-owned.

/sdcard/termux/import/tul/inbox
  Project-owned tul package inbox.

/sdcard/termux/import/tul/package-quarantine/tul
  Project-owned quarantine for moved package archives.
```

## Plan first

```bash
tul clean packages
```

The dry-run separates:

- valid matching tul packages outside the project inbox that can be ingested;
- project-inbox cleanup candidates;
- shared external invalid archives that are report-only.

## Run guarded package cleanup

```bash
tul clean packages run
```

The run form ingests valid matching tul packages from shared external roots into the project inbox and quarantines guarded project-inbox cleanup candidates. It does not move unrelated zip files that lack `tul-package.yml`.

## Quarantine project-inbox cleanup candidates

The run form is limited to project-inbox cleanup candidates such as older duplicate matching package archives or invalid package archives already inside the tul project inbox. Files are moved, not deleted.

## External invalid archives

Invalid zip files in shared roots such as `/sdcard/Download` are report-only by default. Examples include fonts, Android NDK downloads, subtitles, other project archives, and manually created source/review bundles.

Do not quarantine shared external invalid archives just because they lack a root `tul-package.yml`.

## Normal sequence

```bash
tul clean packages
tul clean packages run
tul clean packages
tul package
```

Run cleanup only when the plan shows valid matching packages to ingest or project-inbox cleanup candidates.
