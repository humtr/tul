# Source export specification

Status: accepted and implemented as an explicit Orange-class command after the Stage 7 source-export implementation package closes.

`tul export source` exists as a manual command. It remains separate from `tul update`, `tul verify`, and `tul export review`; automatic source export is still Red class and unapproved.

## Purpose

A source export is a tul-generated full source-context artifact for package generation and code-level diagnosis. It is not review evidence and not backup authority.

It should reduce manual source-archive ambiguity by proving:

- which repo and commit produced the export;
- what root layout the archive uses;
- which files were included and excluded;
- whether the target archive was actually rewritten and verified after replacement.

## Non-goals

A source export must not:

- replace `tul-vf-latest.md` as release-gate evidence;
- replace `tul-review-latest.zip` as compact diff/review transport;
- become a backup or rollback authority;
- run implicitly inside `tul verify`;
- run implicitly inside `tul update` without a later explicit automation decision;
- include `.git`, caches, bytecode, dependency directories, previous zip files, backup files, or transient work roots.

## Implemented command

Command shape:

```text
tul export source [project]
```

Native context rules should match other guarded project commands. No-arg use is allowed only when project inference is unambiguous.

Implemented flags:

```text
--out PATH
--no-state-update
--json
```

The first implementation intentionally does not include untracked files. It exports tracked repository files only, so package generation is tied to committed source context.

## Output path

Default latest output:

```text
/sdcard/termux/import/tul/tul-source-latest.zip
```

Optional timestamped source-export history may be added later, but the first implementation only needs a stable latest artifact if it records enough provenance inside the zip and state/report/handoff.

## Zip root layout

The archive should place repo files at zip root:

```text
README.md
.tul.yml
bin/tul
lib/tulcore/__init__.py
docs/...
```

Do not use a wrapper directory such as:

```text
tul-main/README.md
```

GitHub-generated archives may use wrapper roots and remain valid manual source context. They are not canonical tul source exports.

## Required manifest entry

The zip must contain a machine-readable manifest, tentatively:

```text
source-manifest.json
```

Required fields:

```json
{
  "project": "tul",
  "repo": "humtr/tul",
  "branch": "main",
  "head": "<git rev-parse HEAD>",
  "remote_head": "<git rev-parse origin/main, when available>",
  "working_tree": "clean|dirty",
  "created_at": "<ISO-8601 local timestamp>",
  "command": "tul export source",
  "root_layout": "repo-files-at-zip-root",
  "file_count": 0,
  "size_bytes": 0,
  "sha256": "<sha256 of final zip>",
  "excluded_dirs": [],
  "excluded_suffixes": []
}
```

The implementation stores `payload_sha256` in `source-manifest.json` and records the final archive SHA256 in command output and state metadata. The final zip cannot self-embed its own final SHA256 without changing that SHA256, so `source-manifest.json` sets `sha256` to null and `final_zip_sha256_recorded_externally` to true.

## Default exclusions

Exclude directories:

```text
.git
__pycache__
.pytest_cache
node_modules
dist
build
```

Exclude suffixes:

```text
.pyc
.zip
.bak
```

Exclude runtime/export roots when they are inside the repo. Do not include package work directories, archive roots, temporary verify clones, or generated package zips.

## Validation requirements

The implementation package must prove:

```bash
python3 -m py_compile bin/tul lib/tulcore/*.py
git diff --check
tul package inspect <package.zip>
tul package check <package.zip> --target tul
tul update
```

After update, the latest verify artifact must show:

- Release gate PASS;
- matching HEAD and Remote HEAD;
- clean working tree;
- py_compile PASS;
- git diff --check PASS;
- fresh clone PASS.

Source export validation must additionally prove:

- the output zip exists;
- the output zip is non-empty;
- the output zip is readable by `zipfile` or equivalent;
- required root entries exist, including `README.md`, `.tul.yml`, `bin/tul`, and `lib/tulcore/__init__.py`;
- wrapper-root-only layout is rejected;
- excluded files are absent;
- manifest/provenance fields are present;
- target rewrite and post-replace verification are recorded.

## State and handoff behavior

A successful explicit source export may be recorded in state and surfaced by `tul state` using source-export terminology. It must not appear as:

```text
repo zip
backup
review bundle
release gate
```

A failed source export must not retroactively fail a successful release gate unless source export is the command being tested in that specific package.

## Automation boundary

The first implementation is explicit-only. Automatic post-update source export remains Red class and requires a later decision because it changes default update behavior and may increase runtime cost, storage use, and artifact confusion.

## Export integrity status

`tul export status` is the warning-only inspection surface for source/review export freshness and small docs drift checks. It must not be treated as post-update automation and must not fail the release gate in this stage. Stale source bundles should be refreshed with `tul export source` when a fresh source baseline is needed.
