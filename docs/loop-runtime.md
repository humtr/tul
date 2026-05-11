# tul loop runtime

`tul update <project>` is the default full-loop command.

The intended loop is:

```text
LLM creates package
→ user downloads package
→ tul update <project>
→ tul imports, validates, applies, checks, stages explicit files, commits, pushes, verifies remote HEAD
→ tul prints rollback instructions and an LLM-ready handoff
→ LLM verifies remote state and proposes the next package
```

Split commands are recovery/debug aids. They must not become the default workflow.
