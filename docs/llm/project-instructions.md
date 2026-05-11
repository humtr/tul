# tul project instructions for LLM sessions

Use this repository as the durable source of truth for the Terminal Update Loop.

## Operating role

You are helping maintain `tul`, a local runtime that closes the loop between LLM-generated packages, terminal execution, GitHub remote state, and the next LLM review.

## Required behavior

- Verify remote repo, branch, and HEAD when possible.
- If verification is unavailable, say so explicitly.
- Read current files before proposing implementation.
- Preserve `tul update` push-by-default semantics.
- Do not replace the default workflow with split commands.
- Keep environment paths and project aliases out of engine code.
- Keep project-specific policy in `.tul.yml`.
- Generate cross-platform packages by default.

## Source separation

Separate:

- user-stated goals
- terminal-verified facts
- repo/source-backed facts
- assistant interpretation
- unresolved uncertainty

Do not treat assistant framing as the user's original claim unless the user explicitly accepts it.
