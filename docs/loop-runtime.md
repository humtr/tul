# tul Loop Runtime

`tul` is a local loop runtime for AI-assisted repository updates.

The complete loop is:

```text
LLM package
→ user downloads package
→ tul update <project>
→ package discovery/import
→ manifest validation
→ safe apply
→ repo check
→ sweep
→ explicit stage
→ staged check
→ commit
→ push
→ remote HEAD verification
→ rollback hint
→ report
→ handoff output
→ LLM remote review
→ next package
```

`push` is part of `tul update` by default. `--no-push` is the exception.
