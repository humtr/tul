# LLM-side tul commands

These are user-facing command phrases for LLM sessions. They are not necessarily terminal subcommands.

## `/tul next <project>`

Read the repo and propose the next implementation package scope.

Expected output:

- current remote/status summary
- invariant check
- structural debt
- proposed package name
- files to change
- acceptance criteria

## `/tul review <project>`

Review the just-pushed commit and handoff.

Expected output:

- remote HEAD verification if available
- changed files review
- invariant regression check
- defects and risks
- next recommended package boundary

## `/tul package <project>`

Produce the next cross-platform tul package.

Required package shape:

```text
<package>.zip
  tul-package.yml
  files/
  README.md
  apply.sh       # fallback during transition
  apply.ps1      # fallback during transition
```

When giving the user the execution command, prefer the explicit latest form if the package will be saved to a configured inbox root:

```bash
tul update <project> --latest
# or
tul update <project> -l
```

Use `--package PATH` only for an exact file.

## `/tul roadmap <project>`

Update or review durable planning surfaces:

- `docs/status/current.md`
- `docs/roadmap.md`
- `docs/checklists/loop-runtime.md`

## `/tul verify <project>`

Verify that repo state, handoff, protocol, roadmap, and checklist agree.

## `/tul init-review <project>`

Perform an initial review after clone/init, before proposing implementation.
