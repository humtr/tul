"""Argparse parser construction for the tul command surface."""
from __future__ import annotations

import argparse

from . import __version__


CANONICAL_COMMANDS = "show, package, update, verify, export, run, clean, recover, setup"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tul",
        description="Terminal Update Loop",
        epilog=f"Canonical commands: {CANONICAL_COMMANDS}",
    )
    parser.add_argument("--version", action="version", version=f"tul {__version__}")
    sub = parser.add_subparsers(dest="command")

    p = sub.add_parser("show", help="show project state, exports, handoff, report, config, or history")
    p.add_argument("items", nargs="*", help="optional: topic, project/path, or history count")
    p.add_argument("--json", action="store_true", help="print machine-readable data when supported")
    p.add_argument("--full", action="store_true", help="include full handoff details when topic=handoff")

    p = sub.add_parser("package", help="show latest package or inspect/check/create package archives")
    p.add_argument("items", nargs="*", help="optional: list, check, inspect, new, add, zip, show, package path, project/path")
    p.add_argument("--json", action="store_true", help="print machine-readable output when supported")
    p.add_argument("--target", help="project/path alias for package authoring commands")
    p.add_argument("--project", help="target project id when --target is not used")
    p.add_argument("--repo", help="target repo slug when --target is not used")
    p.add_argument("--branch", help="target branch when --target is not used")
    p.add_argument("--message", help="commit message for package new/add")
    p.add_argument("--out", help="output path for package new/zip")
    p.add_argument("--force", action="store_true", help="replace or reuse outputs when supported")

    p = sub.add_parser("update", help="apply, commit, push, and remote-check a package")
    p.add_argument("items", nargs="*", help="optional: dry, package.zip, project/path")
    p.add_argument("--no-commit", action="store_true")
    p.add_argument("--no-push", action="store_true")
    p.add_argument("--allow-dirty", action="store_true")

    p = sub.add_parser("verify", help="verify repo; use 'fresh' to write uploadable verify artifacts")
    p.add_argument("items", nargs="*", help="optional: fresh, local, json, project/path")
    p.add_argument("--clone-root", help="directory for fresh clone verification; defaults to ~/tmp/tul-verify-fresh")
    p.add_argument("--log-dir", help="directory for verify artifacts; defaults to platform log root")
    p.add_argument("--json", action="store_true", help="print machine-readable verification result")

    p = sub.add_parser("export", help="create source/review transport artifacts")
    p.add_argument("kind", nargs="?", choices=["source", "review"], help="artifact kind; omitted exports both source and review")
    p.add_argument("target", nargs="?", help="optional project/path")
    p.add_argument("--out", help="output zip path; valid only with source or review")
    p.add_argument("--no-state-update", action="store_true", help="do not record metadata in latest state")
    p.add_argument("--json", action="store_true", help="print machine-readable source export data")

    p = sub.add_parser("run", help="run one full Terminal Update Loop cycle")
    p.add_argument("items", nargs="*", help="optional: dry, package.zip, project/path")
    p.add_argument("--no-commit", action="store_true")
    p.add_argument("--no-push", action="store_true")
    p.add_argument("--allow-dirty", action="store_true")
    p.add_argument("--no-export", action="store_true", help="skip source/review export after update")

    p = sub.add_parser("clean", help="show or run guarded cleanup plans")
    p.add_argument("scope", nargs="?", choices=["states", "packages", "backups", "run"])
    p.add_argument("action", nargs="?", choices=["run"])
    p.add_argument("target", nargs="?", help="optional project/path")
    p.add_argument("keep", nargs="?", type=int, default=3, help="newest noop states to keep when cleaning states")
    p.add_argument("--json", action="store_true", help="print machine-readable package cleanup data")

    p = sub.add_parser("recover", help="show rollback/resume recovery plans")
    p.add_argument("topic", nargs="?", choices=["rollback", "resume", "apply", "publish"])
    p.add_argument("target", nargs="?", help="optional project/path")
    p.add_argument("commit", nargs="?", help="commit to revert when topic=rollback")

    p = sub.add_parser("setup", help="show setup status or run setup tasks")
    p.add_argument("topic", nargs="?", choices=["init", "install", "use"])
    p.add_argument("target", nargs="?", help="project alias, GitHub slug, or local repo path")
    p.add_argument("--branch", help="expected branch for setup init")
    p.add_argument("--project", help="project alias for setup init")
    p.add_argument("--default", action="store_true", help="also set config.default_project when topic=use")
    p.add_argument("--copy", action="store_true", help="copy launcher instead of symlink when topic=install")
    p.add_argument("--force", action="store_true", help="replace an existing launcher after backup when topic=install")
    p.add_argument("--no-handoff", action="store_true", help="do not print initial-review handoff when topic=init")

    sub.add_parser("help", help="show this help message")
    return parser
