# Source context and future source export

This document prevents one specific ambiguity: source context can be available before tul has an implemented source-export command.

## Current rule

`tul export source` is not implemented in the current CLI. Do not ask the user to run it until a source-export implementation package has been applied and verified.

Current package-generation sessions may still use source context from:

- a GitHub-generated source archive such as `tul-main.zip`;
- a fresh clone at the verified commit;
- a manually created source zip whose generation command, root layout, and intended commit are known.

These are source-context inputs, not tul runtime artifacts.

## Required checks before using manual source context

Before treating a manual archive as package-generation input, check:

1. the runtime baseline from `tul-vf-latest.md`;
2. the archive root layout, for example whether it has a wrapper directory such as `tul-main/`;
3. whether the archive plausibly corresponds to the verified HEAD;
4. whether the files needed for the package are present;
5. whether the source context is being used only for reading/writing package payloads, not as backup evidence.

## Current source-context vocabulary

| Term | Use |
|---|---|
| `tul-main.zip` | Usually a GitHub-generated archive. Valid as manual source context when root layout and intended commit are understood. |
| `tul-review-latest.zip` | Implemented review/diff transport from `tul export review`. Not full source context. |
| `tul-source-latest.zip` | Reserved future latest source-export path. Not currently produced by tul. |
| `tul export source` | Planned future command. Not currently implemented. |

## Future source-export acceptance gate

A future implementation package for `tul export source` must prove:

- the CLI subcommand exists;
- the output path is explicit and predictable;
- repo files are at zip root, not under a wrapper directory;
- `.git`, caches, bytecode, dependency directories, previous zip files, backups, and transient roots are excluded;
- the export records HEAD, remote HEAD when available, branch, created_at, sha256, bytes, and file count;
- package generation docs distinguish source export from review bundle and backup;
- `tul package check`, py_compile, `git diff --check`, release gate, and fresh clone verification pass.

## Boundary

Do not implement source export inside a terminology-only or planning-only package. Source export changes runtime/export behavior and is therefore Orange class. It must serialize after the terminology/spec baseline closes.
