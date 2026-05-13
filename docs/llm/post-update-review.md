# post-run review

After a successful normal loop, the user should upload `tul-vf-latest.md`. For code work, also upload `tul-source-latest.zip` and `tul-review-latest.zip`.

## Expected normal command

```bash
tul run
```

`run` should leave uploadable verification and transport artifacts current.

## Review order

1. Confirm HEAD and Remote HEAD match.
2. Confirm release gate PASS and fresh clone PASS.
3. Check `tul show exports` snapshot for current source/review bundles.
4. Check docs drift warnings.
5. Decide whether the next step is report-only audit, document cleanup, or a code package.

## Package generation

When generating a package, use:

```text
tul-package.yml
README.md
files/
apply.sh
apply.ps1
```

Do not use broad staging or force push. Normal user application is `tul run`.
