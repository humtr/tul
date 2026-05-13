# LLM handoff protocol

A tul LLM handoff is a compact remote-review request. It should contain runtime facts and pointers to repo-resident documents, not a full repo dump.

## Current surfaces

```bash
tul show
tul show handoff
tul show exports
```

Runtime facts in `tul-vf-latest.md` and `tul show` snapshots outrank repo prose.

## Receiver obligations

When receiving a tul LLM handoff, the LLM must:

1. verify HEAD/Remote HEAD, branch, working tree, and release-gate facts from the uploaded verify artifact;
2. read `docs/llm/entrypoint.md`, `docs/status/current.md`, and `docs/roadmap.md` before proposing the next package;
3. preserve push-by-default, no broad staging, no force push, and config/policy separation;
4. check bundle overlap and serialize work when files or acceptance gates conflict;
5. produce one cross-platform package when code or docs changes are requested.

## Normal user command

```bash
tul run
```

Do not ask the user to run stepwise commands unless diagnosing or intentionally decomposing the loop.

## Source and review context

For a successful post-run review, `tul-vf-latest.md` is usually enough. Ask for `tul-source-latest.zip` when producing the next package or diagnosing code-level failures. Ask for `tul-review-latest.zip` when changed-file context is useful.

Use `tul show exports` to determine whether source/review artifacts are current.
