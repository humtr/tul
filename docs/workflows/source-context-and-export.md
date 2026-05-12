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

## Accepted source-export spec boundary

The pre-implementation source-export contract lives in `docs/workflows/source-export-spec.md`. That document is a specification and acceptance gate, not evidence that the command exists.

Until an implementation package closes, these statements remain true:

- `tul export review` is implemented.
- `tul export source` is not implemented.
- `tul-source-latest.zip` is a reserved future output path.
- GitHub-generated source archives may be source context but not tul-proven source exports.

## Boundary

Do not implement source export inside a terminology-only, spec-only, gate-only, or planning-only package. Source export changes runtime/export behavior and is therefore Orange class. It must serialize after the terminology/spec baseline closes.
