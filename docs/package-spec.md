# tul Package Spec

A standard tul package is a single cross-platform archive:

```text
package.zip
  tul-package.yml
  files/
    ...
  README.md
```

`apply.mode: copy` is the default safe path.

Bootstrap-only packages may include both `apply.sh` and `apply.ps1`.
