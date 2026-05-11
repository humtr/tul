# update pipeline

`tul update <project>` performs the full loop:

1. resolve target from alias or path
2. load global config and repo `.tul.yml`
3. enforce branch guard
4. refuse dirty working tree unless recovery mode is explicit
5. fetch and fast-forward when safe
6. discover/import/extract the matching package
7. validate `tul-package.yml`
8. apply files using safe copy only
9. run repo checks and forbidden-pattern checks
10. sweep repo-local backups out to backup storage
11. verify changed files are within manifest `commit.files`
12. stage only explicit manifest files
13. run staged diff check
14. commit
15. push by default
16. fetch and verify local HEAD equals `origin/<branch>`
17. write report and handoff
18. print rollback instructions and handoff
