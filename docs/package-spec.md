# tul package spec

A normal LLM-to-terminal package is a cross-platform archive with this structure:

```text
<package>.zip
  tul-package.yml
  files/
    ... repo-relative files ...
  README.md
```

The manifest must include:

```yaml
version: 1
name: example-package

target:
  project: tul
  repo: humtr/tul
  branch: main

apply:
  mode: copy
  files:
    - from: files/bin/tul
      to: bin/tul

commit:
  files:
    - bin/tul
  message: Example package
```

Only `apply.mode: copy` is supported by the safe default runtime.
