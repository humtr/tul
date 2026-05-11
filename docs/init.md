# tul init

`tul init <id|repo|path>` registers a repository for the loop.

It may:

- clone a GitHub slug when a local repo does not exist
- register or update a project alias in global config
- create `.tul.yml` when missing
- print an initial-review handoff with `--handoff`

It must not silently delete existing config values.
