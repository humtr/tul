# command surface redesign

Stage 7 redesigned the CLI around a small canonical command surface.

## Canonical commands

```text
tul show
tul package
tul update
tul verify
tul export
tul run
tul clean
tul recover
tul setup
```

## Normal loop

```bash
tul run
```

`run` is the only command a normal user needs for the update loop.

Semantics:

```text
package found:
  update -> export -> verify fresh -> show

package not found:
  export -> verify fresh -> show
```

## Stepwise loop

```bash
tul package
tul update
tul export
tul verify fresh
tul show
```

Use the stepwise loop for diagnostics and review only.

## Design boundaries

- `export` creates files only.
- `show` performs status and diagnostic output.
- `verify` checks the repo; `fresh` writes uploadable verify artifacts.
- `update` applies and publishes packages.
- `run` orchestrates the whole loop.

## Smoke coverage

The command surface is now checked by `tul verify fresh` using parser-level smoke checks that do not require project configuration. The smoke checks guard against accidental old top-level command reintroduction and keep `export` file-producing only.
