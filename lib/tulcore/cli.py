"""Command-line interface for tul."""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

from . import __version__
from .checks import run_checks
from .config import config_path, load_global_config, platform_paths, resolve_project
from .errors import TulError
from .gitops import (
    changed_files,
    current_branch,
    fetch,
    head,
    is_dirty,
    pull_ff_only,
    recent_commits,
    remote_head,
    remote_url,
    status_porcelain,
)
from .handoff import generate_handoff
from .init import init_project
from .pipeline import run_update
from .report import build_report
from .state import archive_latest_state, latest_state, summarize_state
from .sweep import sweep_repo


def repo_root_from_module() -> Path:
    return Path(__file__).resolve().parents[2]


def read_repo_text(rel: str, *, repo: Path | None = None) -> str:
    root = repo or repo_root_from_module()
    path = root / rel
    if not path.exists():
        raise TulError(f"missing repo document: {rel}")
    return path.read_text(encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tul", description="Terminal Update Loop")
    parser.add_argument("--version", action="version", version=f"tul {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("init", help="register or initialize a repo for tul")
    p.add_argument("target")
    p.add_argument("--branch")
    p.add_argument("--handoff", action="store_true")

    p = sub.add_parser("status", help="show repo status")
    p.add_argument("target")

    p = sub.add_parser("sync", help="fetch and pull --ff-only when safe")
    p.add_argument("target")

    p = sub.add_parser("check", help="run repo checks")
    p.add_argument("target")

    p = sub.add_parser("doctor", help="show tul environment diagnostics")
    p.add_argument("target", nargs="?")

    p = sub.add_parser("report", help="print a lightweight report")
    p.add_argument("target")

    p = sub.add_parser("handoff", help="print an LLM handoff")
    p.add_argument("target")
    p.add_argument("--mode", default="initial-review")
    p.add_argument("--full", action="store_true", help="include full loop contract and invariants")
    p.add_argument("--instructions", action="store_true", help="print project instruction template instead of runtime handoff")

    p = sub.add_parser("instructions", help="print the repo-resident LLM project instructions")
    p.add_argument("target", nargs="?", help="optional project/path whose repo contains templates/project-instructions.md")

    p = sub.add_parser("sweep", help="move repo-local tul backups out of the repo")
    p.add_argument("target")

    p = sub.add_parser("update", help="run the full package update loop")
    p.add_argument("target")
    p.add_argument("--package", dest="package_path")
    p.add_argument("-l", "--latest", action="store_true", help="use the newest matching package from configured inbox roots")
    p.add_argument("--no-commit", action="store_true")
    p.add_argument("--no-push", action="store_true")
    p.add_argument("--allow-dirty", action="store_true")

    p = sub.add_parser("publish", help="commit and push already-staged changes")
    p.add_argument("target")
    p.add_argument("-m", "--message", required=False)

    p = sub.add_parser("rollback", help="print a safe rollback command")
    p.add_argument("target")
    p.add_argument("commit", nargs="?")

    p = sub.add_parser("state", help="show latest local tul work state hint")
    p.add_argument("target")

    p = sub.add_parser("config", help="config helpers")
    config_sub = p.add_subparsers(dest="config_command", required=True)
    config_sub.add_parser("path")

    sub.add_parser("projects", help="list configured projects")

    # Scaffolds kept explicit so split commands do not become the default loop.
    p = sub.add_parser("import", help="scaffold: package import is normally part of update")
    p.add_argument("package", nargs="?")
    p = sub.add_parser("apply", help="scaffold: package apply is normally part of update")
    p.add_argument("target")
    p = sub.add_parser("resume", help="scaffold: resume is not yet fully implemented")
    p.add_argument("target")
    p = sub.add_parser("archive", help="archive latest local tul work state")
    p.add_argument("target")

    # Friendly alias for users who type `tul help`.
    sub.add_parser("help", help="show this help message")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return dispatch(args, parser)
    except TulError as exc:
        print(f"tul: error: {exc}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("tul: interrupted", file=sys.stderr)
        return 130


def dispatch(args: argparse.Namespace, parser: argparse.ArgumentParser | None = None) -> int:
    command = args.command

    if command == "help":
        if parser is not None:
            parser.print_help()
        return 0

    if command == "init":
        repo, project = init_project(args.target, branch=args.branch)
        print(f"Initialized {project}: {repo}")
        if args.handoff:
            ctx = resolve_project(project)
            print(generate_handoff(repo=ctx.repo_path, project=ctx.project_id, mode="initial-review", expected_repo=ctx.expected_repo))
        return 0

    if command == "status":
        ctx = resolve_project(args.target)
        print_status(ctx)
        return 0

    if command == "sync":
        ctx = resolve_project(args.target)
        branch = current_branch(ctx.repo_path)
        if is_dirty(ctx.repo_path):
            print("Working tree dirty; fetch only, no pull.")
            fetch(ctx.repo_path, branch)
        else:
            fetch(ctx.repo_path, branch)
            pull_ff_only(ctx.repo_path)
        print_status(ctx)
        return 0

    if command == "check":
        ctx = resolve_project(args.target)
        outputs = run_checks(ctx.repo_path, ctx.repo_config)
        for item in outputs:
            print(item)
            print()
        print("Checks passed.")
        return 0

    if command == "doctor":
        print_doctor(getattr(args, "target", None))
        return 0

    if command == "report":
        ctx = resolve_project(args.target)
        print(build_report(repo=ctx.repo_path, project=ctx.project_id))
        return 0

    if command == "handoff":
        ctx = resolve_project(args.target)
        if args.instructions:
            print(read_repo_text("templates/project-instructions.md", repo=ctx.repo_path))
            return 0
        print(
            generate_handoff(
                repo=ctx.repo_path,
                project=ctx.project_id,
                mode=args.mode,
                expected_repo=ctx.expected_repo,
                full=args.full,
            )
        )
        return 0

    if command == "instructions":
        repo = None
        if getattr(args, "target", None):
            repo = resolve_project(args.target).repo_path
        print(read_repo_text("templates/project-instructions.md", repo=repo))
        return 0

    if command == "sweep":
        ctx = resolve_project(args.target)
        moved = sweep_repo(ctx.repo_path, ctx.global_config)
        print("Sweep moved:")
        print("\n".join(moved) if moved else "nothing")
        return 0

    if command == "update":
        ctx = resolve_project(args.target)
        if args.latest and args.package_path:
            raise TulError("use either --package PATH or --latest, not both")
        # Omitting --package already selects the newest matching package from
        # configured inbox roots. --latest/-l is an explicit, readable alias for
        # that behavior. It does not scan work/archive roots, which may contain
        # stale or already-applied package copies.
        package_path = None if args.latest else args.package_path
        result = run_update(
            ctx,
            package_path=package_path,
            no_commit=args.no_commit,
            no_push=args.no_push,
            allow_dirty=args.allow_dirty,
        )
        print(result.report)
        print("\n--- LLM HANDOFF ---\n")
        print(result.handoff)
        return 0

    if command == "publish":
        ctx = resolve_project(args.target)
        print("publish is recovery/debug only. Use 'tul update' for the default loop.")
        print("Staged files:")
        print("\n".join(changed_files(ctx.repo_path, staged=True)) or "none")
        return 0

    if command == "rollback":
        ctx = resolve_project(args.target)
        commit_id = args.commit or ""
        branch = current_branch(ctx.repo_path)
        print(f"cd {ctx.repo_path}")
        print(f"git revert {commit_id}")
        print(f"git push origin {branch}")
        return 0

    if command == "state":
        ctx = resolve_project(args.target)
        paths = platform_paths(ctx.global_config)
        work_root = paths.get("work_root")
        if not work_root:
            print("No platform.work_root configured.")
            return 0
        found = latest_state(work_root, project=ctx.project_id)
        if not found:
            print(f"No tul state found for project {ctx.project_id} under {work_root}")
            return 0
        path, data = found
        print(summarize_state(path, data))
        if data.get("phase") == "failed":
            print()
            print("Repo status at inspection:")
            branch = current_branch(ctx.repo_path)
            try:
                fetch(ctx.repo_path, branch)
            except Exception:
                pass
            print(f"- HEAD: {head(ctx.repo_path)}")
            print(f"- Remote HEAD: {remote_head(ctx.repo_path, branch) or 'unavailable'}")
            clean = not is_dirty(ctx.repo_path)
            print(f"- Working tree: {'clean' if clean else 'dirty'}")
            if clean:
                print("- Note: the latest failed state may be stale or from a repeated/no-op update attempt.")
        return 0

    if command == "archive":
        ctx = resolve_project(args.target)
        paths = platform_paths(ctx.global_config)
        work_root = paths.get("work_root")
        archive_root = paths.get("archive_root") or paths.get("backup_root")
        if not work_root:
            print("No platform.work_root configured.")
            return 0
        if not archive_root:
            print("No platform.archive_root or platform.backup_root configured.")
            return 0
        archived = archive_latest_state(work_root, archive_root, project=ctx.project_id)
        if not archived:
            print(f"No tul state found for project {ctx.project_id} under {work_root}")
            return 0
        state_path, dest, data = archived
        print(f"Archived latest state for {ctx.project_id}:")
        print(f"- state: {state_path}")
        print(f"- dir: {dest}")
        print(f"- phase: {data.get('phase')}")
        return 0

    if command == "config":
        if args.config_command == "path":
            print(config_path())
            return 0

    if command == "projects":
        config, path = load_global_config()
        print(f"Config: {path}")
        for key, value in (config.get("projects") or {}).items():
            print(f"{key}: {value.get('path') if isinstance(value, dict) else value}")
        return 0

    if command in {"import", "apply", "resume"}:
        print(f"'{command}' is scaffolded for recovery/debug. The default workflow is 'tul update <project>'.")
        return 0

    raise TulError(f"unknown command: {command}")


def print_status(ctx) -> None:
    repo = ctx.repo_path
    branch = current_branch(repo)
    try:
        fetch(repo, branch)
    except Exception:
        pass
    print(f"Project: {ctx.project_id}")
    print(f"Repo: {repo}")
    print(f"Remote: {remote_url(repo) or 'unknown'}")
    print(f"Branch: {branch}")
    print(f"HEAD: {head(repo)}")
    print(f"Remote HEAD: {remote_head(repo, branch) or 'unavailable'}")
    status = status_porcelain(repo)
    print("Working tree: clean" if not status else "Working tree:\n" + status)
    print("Recent commits:")
    for item in recent_commits(repo):
        print(f"- {item}")


def print_doctor(target: str | None = None) -> None:
    config, path = load_global_config()
    paths = platform_paths(config)
    print(f"tul version: {__version__}")
    print(f"python: {sys.executable}")
    print(f"git: {shutil.which('git') or 'not found'}")
    print(f"config path: {path}")
    print(f"config exists: {path.exists()}")
    print("platform paths:")
    for key in ("work_root", "archive_root", "backup_root"):
        value = paths.get(key)
        print(f"- {key}: {value or '(not configured)'}")
    print("inbox roots:")
    roots = paths.get("inbox_roots") or []
    if roots:
        for root in roots:
            print(f"- {root} exists={root.exists()} dir={root.is_dir()}")
    else:
        print("- (none)")
    print("projects:")
    for key, value in (config.get("projects") or {}).items():
        print(f"- {key}: {value.get('path') if isinstance(value, dict) else value}")
    if target:
        ctx = resolve_project(target)
        print("target:")
        print(f"- project: {ctx.project_id}")
        print(f"- repo: {ctx.repo_path}")
        print(f"- branch: {current_branch(ctx.repo_path)}")
        print(f"- dirty: {is_dirty(ctx.repo_path)}")
