"""Command-line interface for tul."""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from . import __version__
from .apply import build_apply_plan, write_apply_plan
from .authoring import (
    add_repo_files_to_package,
    check_package_archive,
    format_package_add,
    format_package_check,
    format_package_summary,
    scaffold_package_dir,
    summarize_package_dir,
    zip_package_dir,
)
from .checks import run_checks
from .config import config_path, load_global_config, platform_paths, resolve_project
from .context import active_project, context_path, format_current_context, format_inference_summary, format_inference_warnings, infer_mutating_project, infer_project, set_active_project, set_default_project
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
from .manifest import validate_manifest
from .package import candidate_record, discover_candidates, discover_package_inventory, import_package, invalid_candidate_record, manifest_data_from_archive, select_package, sha256_file
from .pipeline import run_update
from .report import build_report
from .state import archive_latest_state, archive_states, iter_states, latest_state, latest_state_with_commit, state_commit, summarize_compact_state, summarize_state, set_phase
from .sweep import sweep_repo
from .verify import run_verify, write_verify_artifacts


def repo_root_from_module() -> Path:
    return Path(__file__).resolve().parents[2]


def read_repo_text(rel: str, *, repo: Path | None = None) -> str:
    root = repo or repo_root_from_module()
    path = root / rel
    if not path.exists():
        raise TulError(f"missing repo document: {rel}")
    return path.read_text(encoding="utf-8")


def read_project(args, *, command: str):
    inferred = infer_project(getattr(args, "target", None), command=command, read_only=True)
    warnings = format_inference_warnings(inferred)
    if warnings:
        print(warnings)
    return inferred.ctx


def parse_verify_target_and_mode(args) -> tuple[str | None, bool]:
    target = getattr(args, "target", None)
    mode = getattr(args, "mode", None)
    fresh = bool(getattr(args, "fresh_clone", False))
    if target == "fresh" and mode is None:
        return None, True
    if mode == "fresh":
        return target, True
    if mode:
        raise TulError(f"unknown verify mode: {mode}. Use: tul verify fresh")
    return target, fresh


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tul", description="Terminal Update Loop")
    parser.add_argument("--version", action="version", version=f"tul {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("init", help="onboard a repo into the tul loop")
    p.add_argument("target", help="project alias, GitHub slug, or local repo path")
    p.add_argument("--branch", help="expected branch for .tul.yml and update guard")
    p.add_argument("--project", help="project alias to register in global config")
    p.add_argument("--no-handoff", action="store_true", help="do not print the initial-review handoff")
    p.add_argument("--copy-handoff", action="store_true", help="copy handoff to clipboard command when configured")

    p = sub.add_parser("status", help="show repo status")
    p.add_argument("target", nargs="?")

    p = sub.add_parser("sync", help="fetch and pull --ff-only when safe")
    p.add_argument("target")

    p = sub.add_parser("check", help="run repo checks")
    p.add_argument("target", nargs="?")

    p = sub.add_parser("verify", help="verify repo status, checks, docs, and optional fresh clone")
    p.add_argument("target", nargs="?", help="optional project/path, or 'fresh' for fresh-clone verification")
    p.add_argument("mode", nargs="?", help="optional shorthand mode; use 'fresh' for fresh-clone verification")
    p.add_argument("--fresh-clone", action="store_true", help="clone the remote repo into ~/tmp and verify the clone too")
    p.add_argument("--clone-root", help="directory for fresh clone verification; defaults to ~/tmp/tul-verify-fresh")
    p.add_argument("--log-dir", help="directory for verify artifacts; defaults to platform log root")
    p.add_argument("--no-log", action="store_true", help="do not write verify markdown/json artifacts")
    p.add_argument("--json", action="store_true", help="print machine-readable verification result")

    p = sub.add_parser("doctor", help="show tul environment diagnostics")
    p.add_argument("target", nargs="?")

    p = sub.add_parser("install", help="install or resync the user PATH launcher")
    p.add_argument("target", nargs="?", help="project/path to install; defaults to this tul repo")
    p.add_argument("--copy", action="store_true", help="copy launcher instead of creating a symlink on POSIX")
    p.add_argument("--force", action="store_true", help="replace an existing launcher after backing it up")

    p = sub.add_parser("report", help="print a lightweight report")
    p.add_argument("target", nargs="?")

    p = sub.add_parser("handoff", help="print an LLM handoff")
    p.add_argument("target", nargs="?")
    p.add_argument("--mode", default="initial-review")
    p.add_argument("--full", action="store_true", help="include full loop contract and invariants")
    p.add_argument("--instructions", action="store_true", help="print project instruction template instead of runtime handoff")

    p = sub.add_parser("instructions", help="print the repo-resident LLM project instructions")
    p.add_argument("target", nargs="?", help="optional project/path whose repo contains templates/project-instructions.md")

    p = sub.add_parser("use", help="set the active project for later native/default commands")
    p.add_argument("target", help="configured project alias or repo path to use")
    p.add_argument("--default", action="store_true", help="also set config.default_project to this project")

    sub.add_parser("current", help="show active/default/current-directory project context")

    p = sub.add_parser("sweep", help="move repo-local tul backups out of the repo")
    p.add_argument("target")

    p = sub.add_parser("update", help="run the full package update loop")
    p.add_argument("target", nargs="?", help="optional project/path; omitted target uses native context")
    p.add_argument("--package", dest="package_path")
    p.add_argument("-l", "--latest", action="store_true", help="use the newest matching package from configured inbox roots")
    p.add_argument("--no-commit", action="store_true")
    p.add_argument("--no-push", action="store_true")
    p.add_argument("--allow-dirty", action="store_true")
    p.add_argument("--dry-run", action="store_true", help="select/import/validate/plan the package without applying repo changes")
    p.add_argument("--no-verify", action="store_true", help="skip automatic post-update fresh verification")

    p = sub.add_parser("publish", help="commit and push already-staged changes")
    p.add_argument("target")
    p.add_argument("-m", "--message", required=False)


    p = sub.add_parser("package", help="inspect package discovery candidates")
    package_sub = p.add_subparsers(dest="package_command", required=True)

    p_list = package_sub.add_parser("list", help="list matching packages from configured inbox roots")
    p_list.add_argument("target", nargs="?")
    p_list.add_argument("--limit", type=int, default=20, help="maximum candidates to show")
    p_list.add_argument("--json", action="store_true", help="print machine-readable candidate data")

    p_latest = package_sub.add_parser("latest", help="show the newest matching package and selection reason")
    p_latest.add_argument("target", nargs="?")
    p_latest.add_argument("--json", action="store_true", help="print machine-readable selected candidate data")

    p_inspect = package_sub.add_parser("inspect", help="inspect a package archive manifest without applying it")
    p_inspect.add_argument("package_path")
    p_inspect.add_argument("--json", action="store_true", help="print machine-readable package data")

    p_check = package_sub.add_parser("check", help="validate package root layout, manifest, and optional target apply plan")
    p_check.add_argument("package_path")
    p_check.add_argument("--target", help="optional project/path alias to validate target and build apply plan")
    p_check.add_argument("--json", action="store_true", help="print machine-readable check result")

    p_scaffold = package_sub.add_parser("scaffold", help="create a package source directory skeleton")
    p_scaffold.add_argument("name")
    p_scaffold.add_argument("--target", help="project/path alias to infer project/repo/branch")
    p_scaffold.add_argument("--project", help="target project id when --target is not used")
    p_scaffold.add_argument("--repo", help="target repo slug when --target is not used")
    p_scaffold.add_argument("--branch", help="target branch when --target is not used")
    p_scaffold.add_argument("--message", required=True, help="commit message for the package manifest")
    p_scaffold.add_argument("--out", help="output parent directory or package directory; default: current directory")
    p_scaffold.add_argument("--force", action="store_true", help="allow writing into a non-empty package directory")

    p_zip = package_sub.add_parser("zip", help="zip a package source directory with tul-package.yml at archive root")
    p_zip.add_argument("package_dir")
    p_zip.add_argument("--out", help="output zip path; default: <package_dir>.zip")
    p_zip.add_argument("--force", action="store_true", help="replace an existing output zip")

    p_add = package_sub.add_parser("add", help="copy repo files into a package and update its manifest")
    p_add.add_argument("package_dir")
    p_add.add_argument("repo_files", nargs="+", help="repo-relative files to copy into package files/")
    p_add.add_argument("--target", help="project/path alias used as the repo source; defaults to current git repo")
    p_add.add_argument("--message", help="also update commit.message")

    p_summary = package_sub.add_parser("summary", help="summarize a package source directory")
    p_summary.add_argument("package_dir")
    p_summary.add_argument("--json", action="store_true", help="print machine-readable summary")

    p = sub.add_parser("rollback", help="print a safe rollback command")
    p.add_argument("target", nargs="?", help="optional project/path; omitted target uses native context")
    p.add_argument("commit", nargs="?", help="commit to revert; defaults to latest state commit when available")

    p = sub.add_parser("state", help="show local tul work state")
    p.add_argument("target", nargs="?")
    p.add_argument("--all", action="store_true", help="show all matching state files, newest first")
    p.add_argument("--limit", type=int, help="limit displayed states when using --all")
    p.add_argument("--json", action="store_true", help="print state data as JSON")

    p = sub.add_parser("config", help="config helpers")
    config_sub = p.add_subparsers(dest="config_command", required=True)
    config_sub.add_parser("path")

    sub.add_parser("projects", help="list configured projects")

    # Split commands are recovery/debug tools; default workflow remains update.
    p = sub.add_parser("import", help="import, validate, and plan a package without applying it")
    p.add_argument("target", nargs="?", help="optional project/path; omitted target uses native context")
    p.add_argument("--package", dest="package_path")
    p.add_argument("-l", "--latest", action="store_true", help="use newest matching package from configured inbox roots")

    p = sub.add_parser("apply", help="recovery/debug: show how to apply; default workflow remains update")
    p.add_argument("target")
    p.add_argument("--state", help="state.json or work dir to inspect before applying manually")

    p = sub.add_parser("resume", help="recovery/debug: inspect latest state and suggest a safe next command")
    p.add_argument("target")

    p = sub.add_parser("archive", help="archive local tul work state")
    p.add_argument("target")
    p.add_argument("--all", action="store_true", help="archive all matching states, not just the latest")
    p.add_argument("--noop", action="store_true", help="archive no-op states")
    p.add_argument("--imported", action="store_true", help="archive import/validated states without commits")
    p.add_argument("--failed", action="store_true", help="archive failed states")
    p.add_argument("--keep", type=int, default=0, help="keep the newest N selected states and archive the rest")
    p.add_argument("--dry-run", action="store_true", help="show what would be archived without moving files")

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
        result = init_project(args.target, branch=args.branch, project=args.project)
        print(result.summary())
        if not args.no_handoff:
            ctx = resolve_project(result.project_id)
            handoff = generate_handoff(repo=ctx.repo_path, project=ctx.project_id, mode="initial-review", expected_repo=ctx.expected_repo)
            print("\n--- INITIAL REVIEW HANDOFF ---\n")
            print(handoff)
            if args.copy_handoff:
                copied = copy_to_clipboard(handoff, ctx.global_config)
                print(f"\nClipboard: {copied}")
        return 0

    if command == "install":
        repo = resolve_project(args.target).repo_path if getattr(args, "target", None) else repo_root_from_module()
        print(install_launcher(repo, copy=getattr(args, "copy", False), force=getattr(args, "force", False)))
        return 0

    if command == "status":
        ctx = read_project(args, command="status")
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
        ctx = read_project(args, command="check")
        outputs = run_checks(ctx.repo_path, ctx.repo_config)
        for item in outputs:
            print(item)
            print()
        print("Checks passed.")
        return 0

    if command == "verify":
        target, fresh_clone = parse_verify_target_and_mode(args)
        args.target = target
        ctx = read_project(args, command="verify")
        result = run_verify(
            ctx,
            fresh_clone=fresh_clone,
            clone_root=Path(args.clone_root).expanduser() if args.clone_root else None,
        )
        artifacts = None
        if not getattr(args, "no_log", False):
            artifacts = write_verify_artifacts(
                ctx,
                result,
                fresh_clone=fresh_clone,
                log_dir=Path(args.log_dir).expanduser() if args.log_dir else None,
            )
        if args.json:
            payload = result.to_dict()
            if artifacts:
                payload["artifacts"] = artifacts
            print(json.dumps(payload, indent=2, ensure_ascii=False))
        else:
            print(result.to_text(artifacts))
        return 0 if result.ok else 1

    if command == "doctor":
        print_doctor(getattr(args, "target", None))
        return 0

    if command == "report":
        ctx = read_project(args, command="report")
        print(build_report(repo=ctx.repo_path, project=ctx.project_id))
        return 0

    if command == "handoff":
        ctx = read_project(args, command="handoff")
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

    if command == "use":
        ctx = resolve_project(args.target)
        context_file = set_active_project(ctx.project_id, repo_path=ctx.repo_path, set_by=f"tul use {args.target}")
        default_note = "unchanged"
        if getattr(args, "default", False):
            set_default_project(ctx.project_id)
            default_note = ctx.project_id
        print("# tul use")
        print(f"Active project: {ctx.project_id}")
        print(f"Repo: {ctx.repo_path}")
        print(f"Branch: {current_branch(ctx.repo_path)}")
        print(f"Context: {context_file}")
        print(f"Default project: {default_note}")
        print("Next:")
        print("- tul current")
        print("- tul status")
        print("- tul update")
        print("- tul verify fresh")
        return 0

    if command == "current":
        print(format_current_context())
        return 0

    if command == "sweep":
        ctx = resolve_project(args.target)
        moved = sweep_repo(ctx.repo_path, ctx.global_config)
        print("Sweep moved:")
        print("\n".join(moved) if moved else "nothing")
        return 0

    if command == "update":
        inferred = infer_mutating_project(getattr(args, "target", None), command="update")
        ctx = inferred.ctx
        if not getattr(args, "target", None):
            print(format_inference_summary(inferred, command="update"))
            print()
        if args.latest and args.package_path:
            raise TulError("use either --package PATH or --latest, not both")
        # Omitting --package already selects the newest matching package from
        # configured inbox roots. --latest/-l is an explicit, readable alias for
        # that behavior. It does not scan work/archive roots, which may contain
        # stale or already-applied package copies.
        package_path = None if args.latest else args.package_path
        if args.dry_run:
            print_update_dry_run(ctx, package_path=package_path)
            return 0
        result = run_update(
            ctx,
            package_path=package_path,
            no_commit=args.no_commit,
            no_push=args.no_push,
            allow_dirty=args.allow_dirty,
            verify_after=not args.no_verify,
        )
        print(result.report)
        if result.verify_text:
            print("\n--- VERIFY FRESH ---\n")
            print(result.verify_text)
        print("\n--- LLM HANDOFF ---\n")
        print(result.handoff)
        return 0 if result.verify_ok is not False else 1

    if command == "publish":
        ctx = resolve_project(args.target)
        print("publish is recovery/debug only. Use 'tul update' for the default loop.")
        print("Staged files:")
        print("\n".join(changed_files(ctx.repo_path, staged=True)) or "none")
        return 0


    if command == "package":
        if args.package_command == "inspect":
            print_package_inspect(Path(args.package_path), as_json=args.json)
            return 0
        if args.package_command == "check":
            ctx = resolve_project(args.target) if args.target else None
            result = check_package_archive(Path(args.package_path), ctx=ctx)
            if args.json:
                print(json.dumps(result.as_dict(), indent=2, ensure_ascii=False))
            else:
                print(format_package_check(result))
            return 0 if result.ok else 2
        if args.package_command == "scaffold":
            ctx = resolve_project(args.target) if args.target else None
            project = args.project or (ctx.project_id if ctx else None)
            repo = args.repo or (ctx.expected_repo if ctx else None)
            branch = args.branch or (ctx.expected_branch if ctx else None)
            if not project or not repo or not branch:
                raise TulError("package scaffold needs --target or explicit --project --repo --branch")
            out_dir = Path(args.out).expanduser() if args.out else Path.cwd()
            created = scaffold_package_dir(
                args.name,
                out_dir=out_dir,
                project=project,
                repo=repo,
                branch=branch,
                message=args.message,
                force=args.force,
            )
            print("# tul package scaffold")
            print(f"Created: {created}")
            print("Next:")
            print(f"- edit {created / 'tul-package.yml'}")
            print(f"- add files under {created / 'files'}")
            print(f"- tul package zip {created}")
            return 0
        if args.package_command == "zip":
            out = Path(args.out).expanduser() if args.out else None
            archive = zip_package_dir(Path(args.package_dir), out_path=out, force=args.force)
            result = check_package_archive(archive)
            print("# tul package zip")
            print(f"Archive: {archive}")
            print(f"Sha256: {result.sha256}")
            print("Package root: ok")
            print("Next:")
            print(f"- tul package check {archive}")
            return 0
        if args.package_command == "add":
            ctx = resolve_project(args.target) if args.target else None
            result = add_repo_files_to_package(Path(args.package_dir), args.repo_files, repo_path=ctx.repo_path if ctx else None, message=args.message)
            print(format_package_add(result))
            return 0
        if args.package_command == "summary":
            summary = summarize_package_dir(Path(args.package_dir))
            if args.json:
                print(json.dumps(summary, indent=2, ensure_ascii=False))
            else:
                print(format_package_summary(summary))
            return 0
        ctx = read_project(args, command=f"package {args.package_command}")
        if args.package_command == "list":
            print_package_candidates(ctx, limit=args.limit, as_json=args.json, latest_only=False)
            return 0
        if args.package_command == "latest":
            print_package_candidates(ctx, limit=1, as_json=args.json, latest_only=True)
            return 0

    if command == "rollback":
        inferred = infer_mutating_project(getattr(args, "target", None), command="rollback")
        ctx = inferred.ctx
        if not getattr(args, "target", None):
            print(format_inference_summary(inferred, command="rollback"))
            print()
        commit_id = args.commit
        paths = platform_paths(ctx.global_config)
        work_root = paths.get("work_root")
        source = "argument"
        if not commit_id and work_root:
            found = latest_state_with_commit(work_root, project=ctx.project_id)
            if found:
                state_path, data = found
                commit_id = state_commit(data)
                source = f"latest rollbackable state: {state_path}"
        if not commit_id:
            raise TulError("rollback needs a commit argument or at least one rollbackable state with a commit")
        branch = current_branch(ctx.repo_path)
        print("# safe rollback command")
        print(f"# source: {source}")
        print(f"cd {ctx.repo_path}")
        print(f"git revert {commit_id}")
        print(f"git push origin {branch}")
        return 0

    if command == "state":
        ctx = read_project(args, command="state")
        paths = platform_paths(ctx.global_config)
        work_root = paths.get("work_root")
        if not work_root:
            print("No platform.work_root configured.")
            return 0
        if args.all:
            states = iter_states(work_root, project=ctx.project_id)
            total_states = len(states)
            if args.limit is not None:
                states = states[: max(args.limit, 0)]
        else:
            found = latest_state(work_root, project=ctx.project_id)
            states = [found] if found else []
            total_states = len(states)
        if not states:
            print(f"No tul state found for project {ctx.project_id} under {work_root}")
            return 0
        if args.json:
            payload = [{"state_file": str(path), **data} for path, data in states if path is not None]
            print(json.dumps(payload[0] if not args.all else payload, indent=2, ensure_ascii=False))
            return 0
        if not args.all:
            print(summarize_compact_state(work_root, project=ctx.project_id))
            latest_item = states[0]
            if latest_item is not None:
                _, data = latest_item
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
        if args.all and args.limit is not None:
            print(f"Showing {len(states)}/{total_states} state(s) for {ctx.project_id}.")
            print()
        for index, item in enumerate(states):
            if item is None:
                continue
            path, data = item
            if index:
                print("\n---\n")
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
        archived = archive_states(
            work_root,
            archive_root,
            project=ctx.project_id,
            all_states=args.all,
            noop=args.noop,
            imported=args.imported,
            failed=args.failed,
            keep=max(args.keep or 0, 0),
            dry_run=args.dry_run,
        )
        if not archived:
            print(f"No matching tul state found for project {ctx.project_id} under {work_root}")
            print("Examples:")
            print(f"  tul archive {ctx.project_id} --noop --dry-run")
            print(f"  tul archive {ctx.project_id} --noop --keep 3")
            print(f"  tul archive {ctx.project_id} --imported")
            return 0
        action = "Would archive" if args.dry_run else "Archived"
        print(f"{action} {len(archived)} state(s) for {ctx.project_id}:")
        for state_path, dest, data in archived:
            print(f"- state: {state_path}")
            print(f"  dir: {dest}")
            print(f"  phase: {data.get('phase')}")
            if data.get("outcome"):
                print(f"  outcome: {data.get('outcome')}")
            if data.get("commit"):
                print(f"  commit: {data.get('commit')}")
        if args.dry_run:
            print("No files were moved. Re-run without --dry-run to archive.")
        return 0

    if command == "config":
        if args.config_command == "path":
            print(config_path())
            return 0

    if command == "projects":
        config, path = load_global_config()
        active = active_project()
        default = config.get("default_project")
        print(f"Config: {path}")
        print(f"Context: {context_path()}")
        print(f"active_project: {active or '(none)'}")
        print(f"default_project: {default or '(none)'}")
        for key, value in (config.get("projects") or {}).items():
            markers = []
            if key == active:
                markers.append("active")
            if key == default:
                markers.append("default")
            marker = (" [" + ", ".join(markers) + "]") if markers else ""
            print(f"{key}{marker}: {value.get('path') if isinstance(value, dict) else value}")
        return 0

    if command == "import":
        inferred = infer_mutating_project(getattr(args, "target", None), command="import")
        ctx = inferred.ctx
        if not getattr(args, "target", None):
            print(format_inference_summary(inferred, command="import"))
            print()
        if args.latest and args.package_path:
            raise TulError("use either --package PATH or --latest, not both")
        package_path = None if args.latest else args.package_path
        print_import_plan(ctx, package_path=package_path)
        return 0

    if command == "apply":
        ctx = resolve_project(args.target)
        print("'tul apply' is recovery/debug only. The default workflow is 'tul update <project>'.")
        if args.state:
            print(f"State hint: {args.state}")
        print("Recommended safe command:")
        print(f"  tul update {ctx.project_id} -l")
        return 0

    if command == "resume":
        ctx = resolve_project(args.target)
        paths = platform_paths(ctx.global_config)
        work_root = paths.get("work_root")
        found = latest_state(work_root, project=ctx.project_id) if work_root else None
        print("'tul resume' is not automatic yet. Inspect latest state first.")
        if found:
            path, data = found
            print(summarize_state(path, data))
        if work_root:
            rollbackable = latest_state_with_commit(work_root, project=ctx.project_id)
            if rollbackable:
                rollback_path, rollback_data = rollbackable
                print("Latest rollbackable state:")
                print(f"- commit: {rollback_data.get('commit')}")
                print(f"- state: {rollback_path}")
        print("Recommended safe commands:")
        print(f"  tul state {ctx.project_id}")
        print(f"  tul rollback {ctx.project_id}")
        print(f"  tul update {ctx.project_id} -l")
        return 0

    raise TulError(f"unknown command: {command}")





def _package_inventory_for_context(ctx) -> dict:
    branch = current_branch(ctx.repo_path)
    expected_branch = ctx.expected_branch or branch
    inventory = discover_package_inventory(
        ctx.global_config,
        project=ctx.project_id,
        repo=ctx.expected_repo,
        branch=expected_branch,
    )
    return {
        "branch": expected_branch,
        "matching": [candidate_record(item) for item in inventory.matching],
        "incompatible": [candidate_record(item) for item in inventory.incompatible],
        "invalid": [invalid_candidate_record(item) for item in inventory.invalid],
    }


def _candidate_records_for_context(ctx) -> list[dict]:
    return _package_inventory_for_context(ctx)["matching"]


def _duplicate_package_names(records: list[dict]) -> dict[str, list[str]]:
    seen: dict[str, list[str]] = {}
    for item in records:
        seen.setdefault(str(item.get("name") or ""), []).append(str(item.get("path") or ""))
    return {name: paths for name, paths in seen.items() if name and len(paths) > 1}


def print_package_candidates(ctx, *, limit: int = 20, as_json: bool = False, latest_only: bool = False) -> None:
    inventory = _package_inventory_for_context(ctx)
    records = inventory["matching"]
    incompatible = inventory["incompatible"]
    invalid = inventory["invalid"]
    selected = records[0] if records else None
    payload = {
        "project": ctx.project_id,
        "repo": ctx.expected_repo,
        "branch": inventory["branch"],
        "inbox_roots": [str(root) for root in (platform_paths(ctx.global_config).get("inbox_roots") or [])],
        "selection_rule": "newest matching archive by filesystem mtime from configured inbox roots only",
        "selected": selected,
        "duplicates": _duplicate_package_names(records),
        "candidates": records[: max(limit, 0)],
        "incompatible": incompatible[: max(limit, 0)],
        "invalid": invalid[: max(limit, 0)],
        "total_candidates": len(records),
        "total_incompatible": len(incompatible),
        "total_invalid": len(invalid),
    }
    if as_json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return

    title = "# tul package latest" if latest_only else "# tul package list"
    print(title)
    print(f"Project: {ctx.project_id}")
    print(f"Repo: {ctx.expected_repo or '(not configured)'}")
    print(f"Branch: {payload['branch']}")
    print("Selection rule: newest matching archive by mtime from configured inbox roots only")
    print("Inbox roots:")
    for root in payload["inbox_roots"]:
        print(f"- {root}")
    print()
    if not records:
        print("No matching packages found.")
        if incompatible:
            print()
            print("Incompatible package(s) were found:")
            for item in incompatible[: max(limit, 0)]:
                target = item.get("target") or {}
                print(f"- {item.get('path')}")
                print(f"  name: {item.get('name')}")
                print(f"  target: {target.get('project')} {target.get('repo')} {target.get('branch')}")
                print(f"  reason: {item.get('reason')}")
        if invalid:
            print()
            print("Invalid archive(s) ignored:")
            for item in invalid[: max(limit, 0)]:
                print(f"- {item.get('path')}")
                print(f"  reason: {item.get('reason')}")
        print()
        print("Options:")
        print(f"- download a package targeting project={ctx.project_id} repo={ctx.expected_repo} branch={payload['branch']}")
        print(f"- inspect a package: tul package inspect <package.zip>")
        print(f"- use an explicit compatible package: tul update {ctx.project_id} --package <package.zip>")
        return
    print(f"Selected: {selected['path']}")
    print(f"Reason: newest matching candidate; mtime={selected['mtime']}; {selected.get('reason') or 'target match'}")
    duplicates = payload["duplicates"]
    warnings: list[str] = []
    if duplicates:
        for name, paths in duplicates.items():
            warnings.append(f"duplicate matching package name: {name} ({len(paths)} files)")
    if incompatible:
        selected_mtime = float(selected.get("mtime_epoch") or 0)
        newer_incompatible = [item for item in incompatible if float(item.get("mtime_epoch") or 0) > selected_mtime]
        if newer_incompatible:
            warnings.append(f"{len(newer_incompatible)} newer incompatible package(s) exist")
        else:
            warnings.append(f"{len(incompatible)} incompatible package(s) ignored")
    if invalid:
        warnings.append(f"{len(invalid)} invalid archive(s) ignored")
    if warnings:
        print()
        print("Warnings:")
        for item in warnings:
            print(f"- {item}")
        if incompatible:
            print("Incompatible examples:")
            for item in incompatible[:3]:
                target = item.get("target") or {}
                print(f"  - {item.get('path')}")
                print(f"    target: {target.get('project')} {target.get('repo')} {target.get('branch')}")
                print(f"    reason: {item.get('reason')}")
    if latest_only:
        return
    print()
    print(f"Matching candidates shown: {min(limit, len(records))}/{len(records)}")
    for index, item in enumerate(records[: max(limit, 0)], start=1):
        marker = " selected" if index == 1 else ""
        target = item.get("target") or {}
        commit = item.get("commit") or {}
        print(f"[{index}]{marker} {item.get('name')}  {item.get('mtime')}")
        print(f"  path: {item.get('path')}")
        print(f"  target: {target.get('project')} {target.get('repo')} {target.get('branch')}")
        if commit.get("message"):
            print(f"  commit: {commit.get('message')}")
    if incompatible:
        print()
        print(f"Incompatible packages shown: {min(limit, len(incompatible))}/{len(incompatible)}")
        for index, item in enumerate(incompatible[: max(limit, 0)], start=1):
            target = item.get("target") or {}
            print(f"[{index}] {item.get('name')}  {item.get('mtime')}")
            print(f"  path: {item.get('path')}")
            print(f"  target: {target.get('project')} {target.get('repo')} {target.get('branch')}")
            print(f"  reason: {item.get('reason')}")
    if invalid:
        print()
        print(f"Invalid archives shown: {min(limit, len(invalid))}/{len(invalid)}")
        for index, item in enumerate(invalid[: max(limit, 0)], start=1):
            print(f"[{index}] {item.get('name')}  {item.get('mtime')}")
            print(f"  path: {item.get('path')}")
            print(f"  reason: {item.get('reason')}")


def print_package_inspect(package_path: Path, *, as_json: bool = False) -> None:
    path = package_path.expanduser().resolve()
    data = manifest_data_from_archive(path)
    target = data.get("target") or {}
    commit = data.get("commit") or {}
    apply = data.get("apply") or {}
    payload = {
        "path": str(path),
        "sha256": sha256_file(path),
        "name": data.get("name") or path.stem,
        "version": data.get("version"),
        "target": target,
        "apply_mode": apply.get("mode"),
        "apply_files": apply.get("files") or [],
        "commit_message": commit.get("message"),
        "commit_files": commit.get("files") or [],
    }
    if as_json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return
    print("# tul package inspect")
    print(f"Package: {payload['path']}")
    print(f"Name: {payload['name']}")
    print(f"Sha256: {payload['sha256']}")
    print(f"Target: {target.get('project')} {target.get('repo')} {target.get('branch')}")
    print(f"Apply mode: {payload['apply_mode']}")
    print(f"Apply files: {len(payload['apply_files'])}")
    print(f"Commit message: {payload['commit_message']}")
    print("Commit files:")
    for item in payload["commit_files"]:
        print(f"- {item}")


def print_update_dry_run(ctx, *, package_path: str | None = None) -> None:
    print("# tul update dry-run")
    print("No repo files will be modified. This command imports, validates, and builds an apply plan only.")
    print()
    if package_path is None:
        print_package_candidates(ctx, limit=5, as_json=False, latest_only=True)
        print()
    print_import_plan(ctx, package_path=package_path)

def copy_to_clipboard(text: str, config: dict) -> str:
    command = ((config.get("platform") or {}).get("clipboard_command") or "").strip()
    if not command:
        return "not configured"
    try:
        if command == "termux-clipboard-set":
            proc = subprocess.run([command], input=text, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        elif command == "Set-Clipboard":
            proc = subprocess.run(["powershell.exe", "-NoProfile", "-Command", "Set-Clipboard"], input=text, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            proc = subprocess.run(command, input=text, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        if proc.returncode == 0:
            return "copied"
        return f"failed: {proc.stderr.strip() or proc.stdout.strip()}"
    except Exception as exc:
        return f"failed: {exc}"

def print_import_plan(ctx, *, package_path: str | None = None) -> None:
    branch = current_branch(ctx.repo_path)
    expected_branch = ctx.expected_branch or branch
    source = select_package(
        ctx.global_config,
        explicit=package_path,
        project=ctx.project_id,
        repo=ctx.expected_repo,
        branch=expected_branch,
    )
    imported = import_package(source, ctx.global_config)
    state_file = imported.work_dir / "state.json"
    validate_manifest(imported.manifest, project=ctx.project_id, repo=ctx.expected_repo, branch=expected_branch)
    apply_plan = imported.work_dir / "apply-plan.json"
    planned = build_apply_plan(
        imported.manifest,
        extracted_dir=imported.extracted_dir,
        repo_path=ctx.repo_path,
        allowed_files=imported.manifest.commit_files,
    )
    write_apply_plan(apply_plan, planned)
    set_phase(
        state_file,
        "validated",
        outcome="imported",
        project=ctx.project_id,
        repo=str(ctx.repo_path),
        branch=branch,
        package=str(source),
        package_name=imported.manifest.name,
        sha256=imported.sha256,
        apply_plan=str(apply_plan),
        planned_operations=len(planned),
    )
    print("# tul import")
    print(f"Project: {ctx.project_id}")
    print(f"Package: {source}")
    print(f"Work dir: {imported.work_dir}")
    print(f"State file: {state_file}")
    print(f"Apply plan: {apply_plan}")
    print(f"Planned operations: {len(planned)}")
    print("No repo files were modified.")
    print("To run the full safe loop, use:")
    print(f"  tul update {ctx.project_id} --package {source}")

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



def short_path(path: Path | None) -> str:
    return str(path) if path else "not found"


def backup_path(path: Path) -> Path:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return path.with_name(f"{path.name}.bak-{stamp}")


def launcher_version_label(path: Path, *, repo_bin: Path | None = None) -> str:
    """Return a safe launcher version label without spawning nested tul.

    `tul doctor` should not execute `tul --version` recursively. On some
    mobile/Termux environments nested launcher execution can produce confusing
    shell-level abort messages even after diagnostics are printed. If the PATH
    launcher resolves to the target repo launcher, the current module version is
    authoritative. If it does not, report the drift and ask the user to resync.
    """
    if repo_bin is not None and same_resolved(path, repo_bin):
        return f"tul {__version__}"
    return "not checked (launcher is stale, copied, or outside target repo)"


def same_resolved(a: Path | None, b: Path | None) -> bool:
    if not a or not b:
        return False
    try:
        return a.resolve() == b.resolve()
    except Exception:
        return False


def path_launcher_info(repo: Path | None = None) -> list[str]:
    found = shutil.which("tul")
    repo_bin = (repo / "bin" / "tul") if repo else None
    lines = ["launcher:"]
    lines.append(f"- PATH tul: {found or 'not found'}")
    if found:
        found_path = Path(found)
        try:
            lines.append(f"- PATH tul resolved: {found_path.resolve()}")
        except Exception:
            lines.append("- PATH tul resolved: unavailable")
        lines.append(f"- PATH tul version: {launcher_version_label(found_path, repo_bin=repo_bin)}")
    if repo_bin:
        lines.append(f"- repo bin/tul: {repo_bin}")
        lines.append(f"- repo bin/tul version: {launcher_version_label(repo_bin, repo_bin=repo_bin)}")
        if found:
            status = "synced" if same_resolved(Path(found), repo_bin) else "stale-or-copy"
            lines.append(f"- launcher status: {status}")
            if status != "synced":
                lines.append("- suggested fix: tul install " + str(repo))
        else:
            lines.append("- launcher status: missing")
            lines.append("- suggested fix: tul install " + str(repo))
    return lines


def install_launcher(repo: Path, *, copy: bool = False, force: bool = False) -> str:
    repo = repo.resolve()
    repo_launcher = repo / "bin" / "tul"
    if not repo_launcher.exists():
        raise TulError(f"missing repo launcher: {repo_launcher}")

    home_bin = Path.home() / "bin"
    home_bin.mkdir(parents=True, exist_ok=True)
    lines = ["# tul install"]
    lines.append(f"Repo: {repo}")
    lines.append(f"Repo launcher: {repo_launcher}")

    if os.name == "nt":
        cmd = home_bin / "tul.cmd"
        content = f'@echo off\r\n"{sys.executable}" "{repo_launcher}" %*\r\n'
        if cmd.exists() and cmd.read_text(encoding="utf-8", errors="ignore") != content:
            if not force:
                lines.append(f"Existing launcher differs: {cmd}")
                lines.append("Re-run with --force to back it up and replace it.")
                return "\n".join(lines)
            backup = backup_path(cmd)
            shutil.move(str(cmd), str(backup))
            lines.append(f"Backed up existing launcher: {backup}")
        cmd.write_text(content, encoding="utf-8")
        lines.append(f"Installed Windows launcher: {cmd}")
        path_entries = os.environ.get("PATH", "").split(os.pathsep)
        if str(home_bin) not in path_entries:
            lines.append(f"NOTE: add this directory to PATH if needed: {home_bin}")
        lines.extend(path_launcher_info(repo))
        return "\n".join(lines)

    launcher = home_bin / "tul"
    if launcher.exists() or launcher.is_symlink():
        if launcher.is_symlink() and same_resolved(launcher, repo_launcher):
            lines.append(f"Launcher already synced: {launcher} -> {repo_launcher}")
            lines.extend(path_launcher_info(repo))
            return "\n".join(lines)
        if launcher.is_symlink():
            launcher.unlink()
            lines.append(f"Removed stale symlink launcher: {launcher}")
        else:
            backup = backup_path(launcher)
            shutil.move(str(launcher), str(backup))
            lines.append(f"Backed up existing non-symlink launcher: {backup}")
    if copy:
        shutil.copy2(repo_launcher, launcher)
        lines.append(f"Copied launcher: {launcher}")
    else:
        launcher.symlink_to(repo_launcher)
        lines.append(f"Symlinked launcher: {launcher} -> {repo_launcher}")
    repo_launcher.chmod(repo_launcher.stat().st_mode | 0o755)
    try:
        launcher.chmod(launcher.stat().st_mode | 0o755)
    except Exception:
        pass
    path_entries = os.environ.get("PATH", "").split(os.pathsep)
    if str(home_bin) not in path_entries:
        lines.append(f"NOTE: add this directory to PATH if needed: {home_bin}")
        lines.append('For Termux/bash: export PATH="$HOME/bin:$PATH"')
    lines.extend(path_launcher_info(repo))
    return "\n".join(lines)


def print_doctor(target: str | None = None) -> None:
    config, path = load_global_config()
    paths = platform_paths(config)
    print(f"tul version: {__version__}")
    print(f"python: {sys.executable}")
    print(f"git: {shutil.which('git') or 'not found'}")
    print(f"config path: {path}")
    print(f"config exists: {path.exists()}")
    print("platform paths:")
    for key in ("work_root", "archive_root", "log_root", "backup_root"):
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
    ctx = None
    print("runtime context:")
    print(f"- context path: {context_path()}")
    print(f"- active_project: {active_project() or '(none)'}")
    print(f"- default_project: {config.get('default_project') or '(none)'}")
    if target:
        ctx = resolve_project(target)
        print("target:")
        print(f"- project: {ctx.project_id}")
        print(f"- repo: {ctx.repo_path}")
        print(f"- branch: {current_branch(ctx.repo_path)}")
        print(f"- dirty: {is_dirty(ctx.repo_path)}")
    print("launcher diagnostics:")
    repo = ctx.repo_path if ctx else None
    for line in path_launcher_info(repo):
        print(line)
