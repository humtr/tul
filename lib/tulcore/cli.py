from __future__ import annotations

import argparse
import subprocess
import sys

from .checks import run_checks
from .config import load_global, load_repo
from .errors import TulError
from .gitops import sync
from .handoff import build as build_handoff
from .init import init_project
from .pipeline import resolve, run_publish, run_update
from .report import report_text, status_text
from .sweep import sweep


def repo_cfg(target: str):
    cfg = load_global()
    repo = resolve(target, cfg)
    rcfg = load_repo(repo)
    return cfg, repo, rcfg


def cmd_init(args):
    init_project(args.target, branch=args.branch, handoff=args.handoff)


def cmd_status(args):
    _cfg, repo, rcfg = repo_cfg(args.target)
    print(status_text(repo, rcfg.get("name"), rcfg))


def cmd_sync(args):
    _cfg, repo, _rcfg = repo_cfg(args.target)
    print(sync(repo))


def cmd_check(args):
    _cfg, repo, rcfg = repo_cfg(args.target)
    run_checks(repo, rcfg)
    print("Checks passed.")


def cmd_report(args):
    _cfg, repo, rcfg = repo_cfg(args.target)
    print(report_text(repo, rcfg.get("name"), rcfg))


def cmd_handoff(args):
    _cfg, repo, rcfg = repo_cfg(args.target)
    print(build_handoff(repo, rcfg.get("name"), rcfg))


def cmd_update(args):
    run_update(args.target, args.package, args.no_commit, args.no_push)


def cmd_publish(args):
    run_publish(args.target, args.files, args.message, args.no_push)


def cmd_sweep(args):
    cfg, repo, rcfg = repo_cfg(args.target)
    sweep(repo, cfg, rcfg.get("name") or repo.name)


def cmd_projects(args):
    cfg = load_global()
    if not cfg.projects:
        print("No projects registered.")
    for name, entry in cfg.projects.items():
        print(f"{name}: {entry.get('path') if isinstance(entry, dict) else entry}")


def cmd_config_path(args):
    print(load_global().path)


def parser():
    p = argparse.ArgumentParser(prog="tul")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("init")
    s.add_argument("target")
    s.add_argument("--branch")
    s.add_argument("--handoff", action="store_true")
    s.set_defaults(func=cmd_init)

    for name, func in [
        ("status", cmd_status),
        ("sync", cmd_sync),
        ("check", cmd_check),
        ("verify", cmd_check),
        ("report", cmd_report),
        ("handoff", cmd_handoff),
        ("sweep", cmd_sweep),
    ]:
        sp = sub.add_parser(name)
        sp.add_argument("target")
        sp.set_defaults(func=func)

    s = sub.add_parser("update")
    s.add_argument("target")
    s.add_argument("--package", default="latest")
    s.add_argument("--no-commit", action="store_true")
    s.add_argument("--no-push", action="store_true")
    s.set_defaults(func=cmd_update)

    s = sub.add_parser("publish")
    s.add_argument("target")
    s.add_argument("--files", nargs="+", required=True)
    s.add_argument("--message", required=True)
    s.add_argument("--no-push", action="store_true")
    s.set_defaults(func=cmd_publish)

    s = sub.add_parser("projects")
    s.set_defaults(func=cmd_projects)

    s = sub.add_parser("config")
    csub = s.add_subparsers(dest="config_cmd", required=True)
    sp = csub.add_parser("path")
    sp.set_defaults(func=cmd_config_path)

    return p


def main(argv=None) -> int:
    p = parser()
    args = p.parse_args(argv)
    try:
        args.func(args)
        return 0
    except TulError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    except subprocess.CalledProcessError as exc:
        print(f"ERROR: command failed with exit code {exc.returncode}: {exc.cmd}", file=sys.stderr)
        if exc.stdout:
            print(exc.stdout, file=sys.stderr)
        if exc.stderr:
            print(exc.stderr, file=sys.stderr)
        return exc.returncode or 1
