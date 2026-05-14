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
from typing import Any

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
from .context import (
    active_project,
    context_path,
    format_current_context,
    format_inference_summary,
    format_inference_warnings,
    infer_mutating_project,
    infer_project,
    set_active_project,
    set_default_project,
)
from .errors import TulError
from .cli_parser import CANONICAL_COMMANDS, build_parser
from .gitops import (
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
from .integrity import export_integrity_data, format_export_integrity
from .manifest import validate_manifest
from .package import (
    candidate_record,
    discover_package_inventory,
    import_package,
    invalid_candidate_record,
    manifest_data_from_archive,
    select_package,
    sha256_file,
)
from .package_hygiene import format_package_hygiene, run_package_hygiene
from .pipeline import run_update
from .report import build_report
from .review import export_review_bundle, format_review_export
from .source import export_source_bundle, format_source_export
from .state import (
    archive_inventory,
    archive_protected_paths,
    archive_selector_label,
    archive_states,
    iter_states,
    latest_state,
    latest_state_with_commit,
    state_commit,
    summarize_compact_state,
    summarize_state,
    set_phase,
)
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

def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command is None:
        args.command = "show"
        args.topic = None
        args.target = None
        args.count = None
        args.json = False
        args.full = False
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
    if command == "show":
        return command_show(args)
    if command == "package":
        return command_package(args)
    if command == "update":
        return command_update(args)
    if command == "verify":
        return command_verify(args)
    if command == "export":
        return command_export(args)
    if command == "run":
        return command_run(args)
    if command == "clean":
        return command_clean(args)
    if command == "recover":
        return command_recover(args)
    if command == "setup":
        return command_setup(args)
    raise TulError(f"unknown command: {command}. Canonical commands: {CANONICAL_COMMANDS}")


# ----- canonical command handlers -------------------------------------------------


def command_show(args: argparse.Namespace) -> int:
    topic, target, count = parse_show_items(args.items)
    args.target = target
    if topic == "state":
        ctx = read_project(args, command="show")
        print_show_state(ctx, as_json=getattr(args, "json", False))
        return 0
    if topic == "exports":
        ctx = read_project(args, command="show exports")
        if getattr(args, "json", False):
            print(json.dumps(export_integrity_data(ctx), indent=2, ensure_ascii=False))
        else:
            print(format_export_integrity(ctx))
        return 0
    if topic == "handoff":
        ctx = read_project(args, command="show handoff")
        print(generate_handoff(repo=ctx.repo_path, project=ctx.project_id, mode="initial-review", expected_repo=ctx.expected_repo, full=args.full))
        return 0
    if topic == "report":
        ctx = read_project(args, command="show report")
        print(build_report(repo=ctx.repo_path, project=ctx.project_id))
        return 0
    if topic == "projects":
        print_projects()
        return 0
    if topic == "config":
        print(format_current_context())
        print(f"config path: {config_path()}")
        return 0
    if topic == "history":
        ctx = read_project(args, command="show history")
        print_state_history(ctx, limit=count or 5, as_json=args.json)
        return 0
    if topic == "instructions":
        repo = resolve_project(target).repo_path if target else None
        print(read_repo_text("templates/project-instructions.md", repo=repo))
        return 0
    raise TulError(f"unknown show topic: {topic}")


def command_package(args: argparse.Namespace) -> int:
    sub, rest = parse_package_items(args.items)
    if sub is None:
        target = rest[0] if rest else None
        args.target = target
        ctx = read_project(args, command="package")
        print_package_candidates(ctx, limit=1, as_json=args.json, latest_only=True)
        return 0
    if sub == "list":
        target = rest[0] if rest else None
        limit = int(rest[1]) if len(rest) > 1 and str(rest[1]).isdigit() else 20
        args.target = target
        ctx = read_project(args, command="package list")
        print_package_candidates(ctx, limit=limit, as_json=args.json, latest_only=False)
        return 0
    if sub == "inspect":
        if not rest:
            raise TulError("package inspect requires <package.zip>")
        print_package_inspect(Path(rest[0]), as_json=args.json)
        return 0
    if sub == "check":
        if not rest:
            raise TulError("package check requires <package.zip>")
        target = args.target or (rest[1] if len(rest) > 1 else None)
        ctx = resolve_project(target) if target else None
        result = check_package_archive(Path(rest[0]), ctx=ctx)
        print(json.dumps(result.as_dict(), indent=2, ensure_ascii=False) if args.json else format_package_check(result))
        return 0 if result.ok else 2
    if sub == "new":
        if not rest:
            raise TulError("package new requires <name>")
        if not args.message:
            raise TulError("package new requires --message")
        ctx = resolve_project(args.target) if args.target else None
        path = scaffold_package_dir(
            rest[0],
            out=Path(args.out).expanduser() if args.out else Path.cwd(),
            project=args.project or (ctx.project_id if ctx else None),
            repo=args.repo or (ctx.expected_repo if ctx else None),
            branch=args.branch or (ctx.expected_branch if ctx else None),
            message=args.message,
            force=args.force,
        )
        print(f"Created package skeleton: {path}")
        return 0
    if sub == "add":
        if len(rest) < 2:
            raise TulError("package add requires <package-dir> <repo-file>...")
        ctx = resolve_project(args.target) if args.target else None
        result = add_repo_files_to_package(Path(rest[0]), rest[1:], repo_path=ctx.repo_path if ctx else None, message=args.message)
        print(format_package_add(result))
        return 0
    if sub == "zip":
        if not rest:
            raise TulError("package zip requires <package-dir>")
        archive = zip_package_dir(Path(rest[0]), out=Path(args.out).expanduser() if args.out else None, force=args.force)
        print(f"Created package zip: {archive}")
        return 0
    if sub == "show":
        if not rest:
            raise TulError("package show requires <package-dir>")
        summary = summarize_package_dir(Path(rest[0]))
        print(json.dumps(summary, indent=2, ensure_ascii=False) if args.json else format_package_summary(summary))
        return 0
    raise TulError(f"unknown package command: {sub}")


def command_update(args: argparse.Namespace) -> int:
    target, package_path, dry = parse_target_package_dry(args.items)
    inferred = infer_mutating_project(target, command="update")
    ctx = inferred.ctx
    if target is None:
        print(format_inference_summary(inferred, command="update"))
        print()
    if dry:
        print_update_dry_run(ctx, package_path=package_path)
        return 0
    result = run_update(
        ctx,
        package_path=package_path,
        no_commit=args.no_commit,
        no_push=args.no_push,
        allow_dirty=args.allow_dirty,
        verify_after=False,
        post_export=False,
    )
    print(result.report)
    print("\n--- NEXT ---\n")
    print("Run `tul verify fresh`, `tul export`, and `tul show`, or use `tul run` for the full loop.")
    print("\n--- LLM HANDOFF ---\n")
    print(result.handoff)
    return 0


def command_verify(args: argparse.Namespace) -> int:
    target, mode_json, fresh = parse_verify_items(args.items)
    args.target = target
    ctx = read_project(args, command="verify")
    result = run_verify(
        ctx,
        fresh_clone=fresh,
        clone_root=Path(args.clone_root).expanduser() if args.clone_root else None,
    )
    write_artifacts = fresh
    artifacts = None
    if write_artifacts:
        artifacts = write_verify_artifacts(
            ctx,
            result,
            fresh_clone=True,
            log_dir=Path(args.log_dir).expanduser() if args.log_dir else None,
        )
    if args.json or mode_json:
        payload = result.to_dict()
        if artifacts:
            payload["artifacts"] = artifacts
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(result.to_text(artifacts))
    return 0 if result.ok else 1


def command_export(args: argparse.Namespace) -> int:
    if args.kind is None:
        if args.out:
            raise TulError("--out is only valid with `tul export source` or `tul export review`")
        ctx = read_project(args, command="export")
        source = export_source_bundle(ctx, update_state=not args.no_state_update)
        review = export_review_bundle(ctx, update_state=not args.no_state_update)
        print("# tul export")
        print()
        print(format_source_export(source))
        print()
        print(format_review_export(review))
        return 0
    ctx = read_project(args, command=f"export {args.kind}")
    out_path = Path(args.out).expanduser() if args.out else None
    if args.kind == "source":
        result = export_source_bundle(ctx, out_path=out_path, update_state=not args.no_state_update)
        print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False) if args.json else format_source_export(result))
        return 0
    if args.kind == "review":
        if args.json:
            raise TulError("--json is only supported for `tul export source` in this version")
        result = export_review_bundle(ctx, out_path=out_path, update_state=not args.no_state_update)
        print(format_review_export(result))
        return 0
    raise TulError(f"unknown export kind: {args.kind}")


def command_run(args: argparse.Namespace) -> int:
    target, package_path, dry = parse_target_package_dry(args.items)
    inferred = infer_mutating_project(target, command="run")
    ctx = inferred.ctx
    if target is None:
        print(format_inference_summary(inferred, command="run"))
        print()

    package_available = package_path is not None or has_matching_package(ctx)

    if dry:
        print("# tul run dry")
        print("No repo files will be modified.")
        print()
        if package_available:
            print("Would run update phase:")
            print()
            print_update_dry_run(ctx, package_path=package_path)
        else:
            print("No matching package was found.")
            print("Would skip update and refresh artifacts for the current HEAD.")
        print()
        if not args.no_export:
            print("Would then run: tul export")
        print("Would then run: tul verify fresh")
        print("Verification now includes CLI runtime smoke and regression tests.")
        print("Would then run: tul show")
        return 0

    update_handoff: str | None = None
    source_export = None
    review_export = None
    verify = None
    artifacts = None
    if package_available:
        update = run_update(
            ctx,
            package_path=package_path,
            no_commit=args.no_commit,
            no_push=args.no_push,
            allow_dirty=args.allow_dirty,
            verify_after=False,
            post_export=False,
        )
        print(update.report)
        update_handoff = update.handoff
        can_refresh_artifacts = not args.no_commit and not args.no_push
    else:
        print("# tul run")
        print("No matching package found. Refreshing verification and transport artifacts for the current HEAD.")
        can_refresh_artifacts = True

    if can_refresh_artifacts:
        if not args.no_export:
            print("\n--- EXPORT PRECHECK ---\n")
            source_export = export_source_bundle(ctx, update_state=True)
            review_export = export_review_bundle(ctx, update_state=True)
            print(format_source_export(source_export))
            print()
            print(format_review_export(review_export))
        print("\n--- VERIFY FRESH ---\n")
        verify = run_verify(ctx, fresh_clone=True)
        artifacts = write_verify_artifacts(ctx, verify, fresh_clone=True)
        print(verify.to_text(artifacts))
        ok = verify.ok
        if ok and not args.no_export:
            print("\n--- EXPORT FINAL ---\n")
            # Review bundles are canonical current-HEAD evidence. Re-export after
            # verify so the bundle contains the head-tagged verify markdown for
            # the same commit rather than a missing or previous-run marker.
            review_export = export_review_bundle(ctx, update_state=True)
            print(format_review_export(review_export))
    else:
        ok = True
        print("\n--- SKIPPED VERIFY/EXPORT ---\n")
        print("Commit or push was disabled; run `tul export` and `tul verify fresh` manually when appropriate.")

    print("\n--- SHOW ---\n")
    print_show_state(ctx, as_json=False)
    if update_handoff:
        print("\n--- LLM HANDOFF ---\n")
        print(update_handoff)
    else:
        print("\n--- LLM HANDOFF ---\n")
        print(generate_handoff(repo=ctx.repo_path, project=ctx.project_id, mode="verify-snapshot", expected_repo=ctx.expected_repo))
    if verify is not None:
        print("\n--- FINAL DECISION ---\n")
        print(format_run_final_summary(ctx, verify=verify, source=source_export, review=review_export, artifacts=artifacts))
    return 0 if ok else 1


def format_run_final_summary(ctx, *, verify, source=None, review=None, artifacts=None, skipped: bool = False) -> str:
    """Return the last, decision-oriented block printed by `tul run`."""
    data = export_integrity_data(ctx)
    source_data = data.get("source_bundle") or {}
    review_data = data.get("review_bundle") or {}
    docs_data = data.get("docs_drift") or {}
    warnings = data.get("warnings") or []

    def step_ok(name: str) -> str:
        for step in getattr(verify, "steps", []):
            if step.name.endswith(name):
                return "PASS" if step.ok else "FAIL"
        return "SKIPPED" if skipped else "MISSING"

    release = "PASS" if getattr(verify, "ok", False) else "FAIL"
    source_status = source_data.get("status") or "skipped"
    review_status = review_data.get("status") or "skipped"
    docs_status = docs_data.get("status") or "unknown"
    warning_status = "none" if not warnings else f"{len(warnings)} warning(s)"
    upload_files: list[tuple[str, str]] = []
    if source is not None and getattr(source, "upload_aliases", None):
        alias = source.upload_aliases.get("root_alias")
        if alias:
            upload_files.append(("source", alias))
    if review is not None and getattr(review, "upload_aliases", None):
        alias = review.upload_aliases.get("root_alias")
        if alias:
            upload_files.append(("review", alias))
    if artifacts and artifacts.get("upload_markdown"):
        upload_files.append(("verify", artifacts["upload_markdown"]))
    upload_labels = {label for label, _ in upload_files}
    upload_status = "ready" if {"source", "review", "verify"}.issubset(upload_labels) else "incomplete"
    final_ok = (
        release == "PASS"
        and step_ok("CLI runtime smoke") == "PASS"
        and step_ok("regression tests") == "PASS"
        and source_status == "current"
        and review_status == "current"
        and docs_status == "clean"
        and warning_status == "none"
        and upload_status == "ready"
    )

    lines = [
        "# tul run final",
        f"Decision: {'PASS' if final_ok else 'CHECK'}",
        f"HEAD: {data.get('head') or getattr(verify, 'head', None) or 'unknown'}",
        f"Remote HEAD: {data.get('remote_head') or getattr(verify, 'remote_head', None) or 'unknown'}",
        "",
        "Gates: "
        f"release={release}; "
        f"cli-smoke={step_ok('CLI runtime smoke')}; "
        f"regression={step_ok('regression tests')}",
        "Artifacts: "
        f"source={source_status}; "
        f"review={review_status}; "
        f"docs={docs_status}; "
        f"warnings={warning_status}; "
        f"upload={upload_status}",
        "",
        "Upload these files:",
    ]
    if upload_files:
        for label, path in upload_files:
            lines.append(f"- {label}: {path}")
    else:
        lines.append("- none")
    lines.append("Note: root latest artifacts are removed; upload the three head-tagged files above.")
    if warnings:
        lines.extend(["", "Warning details:"])
        lines.extend(f"- {item}" for item in warnings)
    return "\n".join(lines)


def command_clean(args: argparse.Namespace) -> int:
    scope = args.scope or "summary"
    run = args.scope == "run" or args.action == "run"
    target = args.target
    keep = args.keep

    # Parser compatibility for the documented form:
    #   tul clean states run 3
    # The third positional slot is named target so project/path can still be
    # supplied for non-active projects. If that slot is a bare integer, treat
    # it as the keep count instead of a project target.
    if target and target.isdigit():
        keep = int(target)
        target = None

    if scope == "summary":
        ctx = read_project(args, command="clean")
        print("# tul clean")
        print("Default mode: plan only. No files were moved.")
        print()
        print_clean_states(ctx, keep=keep, dry_run=True)
        print()
        print_clean_packages(ctx, as_json=args.json, run=False)
        print()
        print("To move guarded cleanup candidates, use: tul clean states run [keep] or tul clean packages run")
        return 0
    ctx = infer_mutating_project(target, command="clean").ctx if run else read_project(args, command=f"clean {scope}")
    if scope == "states" or scope == "run":
        print_clean_states(ctx, keep=keep, dry_run=not run)
        return 0
    if scope == "packages":
        print_clean_packages(ctx, as_json=args.json, run=run)
        return 0
    if scope == "backups":
        if not run:
            print("# tul clean backups")
            print("Default mode: plan only. No files were moved.")
            print(f"Repo: {ctx.repo_path}")
            print("Scope: repo-local tul backup files/directories")
            print("Run `tul clean backups run` to move guarded repo-local tul backups out of the repo.")
            return 0
        moved = sweep_repo(ctx.repo_path, ctx.global_config)
        print("# tul clean backups")
        print("Moved:")
        print("\n".join(moved) if moved else "nothing")
        return 0
    raise TulError(f"unknown clean scope: {scope}")


def command_recover(args: argparse.Namespace) -> int:
    topic = args.topic or "summary"
    ctx = read_project(args, command="recover") if topic == "summary" else infer_mutating_project(args.target, command=f"recover {topic}").ctx
    if topic == "summary":
        print_recover_summary(ctx)
        return 0
    if topic == "rollback":
        print_rollback_plan(ctx, commit_id=args.commit)
        return 0
    if topic == "resume":
        print_resume_plan(ctx)
        return 0
    if topic == "apply":
        print("# tul recover apply")
        print("This command does not modify the repo. Use `tul update` for the normal update path.")
        print(f"Repo: {ctx.repo_path}")
        print("Suggested:")
        print("  tul update dry")
        print("  tul update")
        return 0
    if topic == "publish":
        print("# tul recover publish")
        print("This command does not commit or push. Use `tul update` for normal publishing.")
        print("Staged files:")
        print("\n".join(changed_staged(ctx.repo_path)) or "none")
        return 0
    raise TulError(f"unknown recover topic: {topic}")


def command_setup(args: argparse.Namespace) -> int:
    topic = args.topic or "summary"
    if topic == "summary":
        print_setup_summary(getattr(args, "target", None))
        return 0
    if topic == "init":
        if not args.target:
            raise TulError("setup init requires a project alias, GitHub slug, or local repo path")
        result = init_project(args.target, branch=args.branch, project=args.project)
        print(result.summary())
        if not args.no_handoff:
            ctx = resolve_project(result.project_id)
            print("\n--- INITIAL REVIEW HANDOFF ---\n")
            print(generate_handoff(repo=ctx.repo_path, project=ctx.project_id, mode="initial-review", expected_repo=ctx.expected_repo))
        return 0
    if topic == "install":
        repo = resolve_project(args.target).repo_path if args.target else repo_root_from_module()
        print(install_launcher(repo, copy=args.copy, force=args.force))
        return 0
    if topic == "use":
        if not args.target:
            raise TulError("setup use requires a configured project alias or repo path")
        ctx = resolve_project(args.target)
        context_file = set_active_project(ctx.project_id, repo_path=ctx.repo_path, set_by=f"tul setup use {args.target}")
        default_note = "unchanged"
        if args.default:
            set_default_project(ctx.project_id)
            default_note = ctx.project_id
        print("# tul setup use")
        print(f"Active project: {ctx.project_id}")
        print(f"Repo: {ctx.repo_path}")
        print(f"Branch: {current_branch(ctx.repo_path)}")
        print(f"Context: {context_file}")
        print(f"Default project: {default_note}")
        print("Next: tul show, tul package, tul run")
        return 0
    raise TulError(f"unknown setup topic: {topic}")


# ----- parsing helpers ------------------------------------------------------------


def parse_show_items(items: list[str]) -> tuple[str, str | None, int | None]:
    topics = {"state", "exports", "handoff", "report", "projects", "config", "history", "instructions"}
    if not items:
        return "state", None, None
    if items[0] in topics:
        topic = items[0]
        rest = items[1:]
    else:
        topic = "state"
        rest = items
    target: str | None = None
    count: int | None = None
    for item in rest:
        if topic == "history" and str(item).isdigit():
            count = int(item)
        elif target is None:
            target = item
        else:
            raise TulError(f"too many arguments for show {topic}: {' '.join(items)}")
    return topic, target, count


def parse_package_items(items: list[str]) -> tuple[str | None, list[str]]:
    commands = {"list", "check", "inspect", "new", "add", "zip", "show"}
    if not items:
        return None, []
    if items[0] in commands:
        return items[0], items[1:]
    return None, items


def _looks_like_zip(value: str) -> bool:
    return value.endswith(".zip") or Path(value).expanduser().suffix == ".zip"


def parse_target_package_dry(items: list[str]) -> tuple[str | None, str | None, bool]:
    target: str | None = None
    package_path: str | None = None
    dry = False
    for item in items:
        if item == "dry":
            dry = True
        elif _looks_like_zip(item):
            if package_path is not None:
                raise TulError("only one package zip may be specified")
            package_path = item
        else:
            if target is not None:
                raise TulError("only one project/path target may be specified")
            target = item
    return target, package_path, dry


def parse_verify_items(items: list[str]) -> tuple[str | None, bool, bool]:
    target: str | None = None
    fresh = False
    mode_json = False
    for item in items:
        if item == "fresh":
            fresh = True
        elif item in {"local", "quick"}:
            fresh = False
        elif item == "json":
            mode_json = True
        else:
            if target is not None:
                raise TulError("only one project/path target may be specified")
            target = item
    return target, mode_json, fresh


def has_matching_package(ctx) -> bool:
    """Return whether the configured inboxes contain a compatible package for ctx."""
    inventory = _package_inventory_for_context(ctx)
    return bool(inventory.get("matching"))



# ----- display helpers ------------------------------------------------------------


def print_show_state(ctx, *, as_json: bool = False) -> None:
    paths = platform_paths(ctx.global_config)
    work_root = paths.get("work_root")
    branch = current_branch(ctx.repo_path)
    try:
        fetch(ctx.repo_path, branch)
    except Exception:
        pass
    found = latest_state(work_root, project=ctx.project_id) if work_root else None
    payload = {
        "project": ctx.project_id,
        "repo": str(ctx.repo_path),
        "branch": branch,
        "head": head(ctx.repo_path),
        "remote_head": remote_head(ctx.repo_path, branch),
        "working_tree": "dirty" if is_dirty(ctx.repo_path) else "clean",
        "latest_state": str(found[0]) if found else None,
        "latest_state_data": found[1] if found else None,
        "exports": export_integrity_data(ctx),
    }
    if as_json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return
    print("# tul show")
    print()
    print(f"Project: {payload['project']}")
    print(f"Repo: {payload['repo']}")
    print(f"Branch: {payload['branch']}")
    print(f"HEAD: {payload['head']}")
    print(f"Remote HEAD: {payload['remote_head'] or 'unavailable'}")
    print(f"Working tree: {payload['working_tree']}")
    if work_root:
        print()
        print(summarize_compact_state(work_root, project=ctx.project_id))
    print()
    print(format_export_integrity(ctx))
    print()
    print("Next:")
    print("- full loop: tul run")
    print("- stepwise: tul package; tul update; tul verify fresh; tul export")
    print("- recovery: tul recover")


def print_state_history(ctx, *, limit: int = 5, as_json: bool = False) -> None:
    paths = platform_paths(ctx.global_config)
    work_root = paths.get("work_root")
    if not work_root:
        print("No platform.work_root configured.")
        return
    states = iter_states(work_root, project=ctx.project_id)[: max(limit, 0)]
    if as_json:
        print(json.dumps([{"state_file": str(path), **data} for path, data in states], indent=2, ensure_ascii=False))
        return
    print(f"# tul show history {limit}")
    if not states:
        print(f"No tul state found for project {ctx.project_id} under {work_root}")
        return
    for index, (path, data) in enumerate(states):
        if index:
            print("\n---\n")
        print(summarize_state(path, data))


def print_projects() -> None:
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


def print_clean_states(ctx, *, keep: int = 3, dry_run: bool = True) -> None:
    paths = platform_paths(ctx.global_config)
    work_root = paths.get("work_root")
    archive_root = paths.get("archive_root") or paths.get("backup_root")
    print("# tul clean states")
    print(f"Project: {ctx.project_id}")
    print(f"Mode: {'plan' if dry_run else 'move'}")
    if not work_root or not archive_root:
        print("No platform.work_root and archive_root/backup_root configured.")
        return
    inventory = archive_inventory(work_root, project=ctx.project_id)
    protected = archive_protected_paths(work_root, project=ctx.project_id)
    archived = archive_states(work_root, archive_root, project=ctx.project_id, noop=True, keep=max(keep, 0), dry_run=dry_run)
    print(f"Work root: {work_root}")
    print(f"Archive root: {archive_root}")
    print(f"Selector: noop")
    print(f"Keep newest selected: {keep}")
    print("Inventory:")
    for key in ("total", "noop", "imported", "failed", "rollbackable"):
        print(f"- {key}: {inventory.get(key)}")
    if protected:
        print("Protected reference states:")
        for key, value in protected.items():
            print(f"- {key}: {value}")
    if not archived:
        print("No matching state directories to move.")
        return
    print()
    print(f"{'Would move' if dry_run else 'Moved'} {len(archived)} state directorie(s):")
    for state_path, dest, data in archived:
        print(f"- {state_path.parent} -> {dest} ({data.get('phase')})")
    if dry_run:
        print("No files were moved. Run `tul clean states run [keep]` to execute this bounded cleanup.")


def print_clean_packages(ctx, *, as_json: bool = False, run: bool = False) -> None:
    result = run_package_hygiene(ctx, ingest=run, quarantine=run)
    if as_json:
        print(json.dumps(result.as_dict(), indent=2, ensure_ascii=False))
    else:
        print(format_package_hygiene(result, limit=50))
        if not run:
            print()
            print("No package files were moved unless the report says mode is executing. Run `tul clean packages run` to ingest/quarantine guarded candidates.")


def print_recover_summary(ctx) -> None:
    print("# tul recover")
    print("This command does not modify the repo. It prints recovery options.")
    print(f"Project: {ctx.project_id}")
    paths = platform_paths(ctx.global_config)
    work_root = paths.get("work_root")
    if work_root:
        latest = latest_state(work_root, project=ctx.project_id)
        if latest:
            print()
            print("Latest state:")
            print(summarize_state(latest[0], latest[1]))
        rollbackable = latest_state_with_commit(work_root, project=ctx.project_id)
        if rollbackable:
            print()
            print("Rollback plan:")
            print_rollback_plan(ctx, commit_id=state_commit(rollbackable[1]), source=f"latest rollbackable state: {rollbackable[0]}")
    print()
    print("Subcommands:")
    print("- tul recover rollback   # print a safe git revert command")
    print("- tul recover resume     # print latest state and safe next commands")
    print("- tul recover apply      # advanced debug; does not modify the repo")
    print("- tul recover publish    # advanced debug; does not commit or push")


def print_rollback_plan(ctx, *, commit_id: str | None = None, source: str | None = None) -> None:
    paths = platform_paths(ctx.global_config)
    work_root = paths.get("work_root")
    if not commit_id and work_root:
        found = latest_state_with_commit(work_root, project=ctx.project_id)
        if found:
            state_path, data = found
            commit_id = state_commit(data)
            source = f"latest rollbackable state: {state_path}"
    if not commit_id:
        raise TulError("rollback needs a commit argument or at least one rollbackable state with a commit")
    branch = current_branch(ctx.repo_path)
    print("# tul recover rollback")
    print("This command does not modify the repo. It prints a safe rollback command.")
    print(f"# source: {source or 'argument'}")
    print(f"cd {ctx.repo_path}")
    print(f"git revert {commit_id}")
    print(f"git push origin {branch}")


def print_resume_plan(ctx) -> None:
    print("# tul recover resume")
    print("This command does not modify the repo. It prints the latest state and safe next commands.")
    paths = platform_paths(ctx.global_config)
    work_root = paths.get("work_root")
    found = latest_state(work_root, project=ctx.project_id) if work_root else None
    if found:
        print(summarize_state(found[0], found[1]))
    print("Recommended safe commands:")
    print("  tul show")
    print("  tul recover rollback")
    print("  tul update dry")
    print("  tul run")


def print_setup_summary(target: str | None = None) -> None:
    config, path = load_global_config()
    paths = platform_paths(config)
    print("# tul setup")
    print(f"tul version: {__version__}")
    print(f"python: {sys.executable}")
    print(f"git: {shutil.which('git') or 'not found'}")
    print(f"config path: {path}")
    print(f"config exists: {path.exists()}")
    print(f"context path: {context_path()}")
    print(f"active_project: {active_project() or '(none)'}")
    print(f"default_project: {config.get('default_project') or '(none)'}")
    print("platform paths:")
    for key in ("work_root", "archive_root", "log_root", "backup_root"):
        print(f"- {key}: {paths.get(key) or '(not configured)'}")
    print("inbox roots:")
    for root in paths.get("inbox_roots") or []:
        print(f"- {root} exists={root.exists()} dir={root.is_dir()}")
    ctx = resolve_project(target) if target else None
    if ctx:
        print("target:")
        print(f"- project: {ctx.project_id}")
        print(f"- repo: {ctx.repo_path}")
        print(f"- branch: {current_branch(ctx.repo_path)}")
        print(f"- dirty: {is_dirty(ctx.repo_path)}")
    print("Subcommands:")
    print("- tul setup init <target>     # register a project")
    print("- tul setup install [target]  # install or refresh launcher")
    print("- tul setup use <project>     # set active project context")
    print("Next: tul show, tul run")
    print("launcher diagnostics:")
    for line in path_launcher_info(ctx.repo_path if ctx else None):
        print(line)


def changed_staged(repo: Path) -> list[str]:
    proc = subprocess.run(["git", "diff", "--cached", "--name-only"], cwd=repo, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0:
        return []
    return [line for line in proc.stdout.splitlines() if line.strip()]


# ----- package/update helpers copied from prior CLI ------------------------------


def _package_inventory_for_context(ctx) -> dict:
    branch = current_branch(ctx.repo_path)
    expected_branch = ctx.expected_branch or branch
    inventory = discover_package_inventory(ctx.global_config, project=ctx.project_id, repo=ctx.expected_repo, branch=expected_branch)
    return {
        "branch": expected_branch,
        "matching": [candidate_record(item) for item in inventory.matching],
        "incompatible": [candidate_record(item) for item in inventory.incompatible],
        "invalid": [invalid_candidate_record(item) for item in inventory.invalid],
    }


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
    title = "# tul package" if latest_only else "# tul package list"
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
            print("\nIncompatible package(s) were found:")
            for item in incompatible[: max(limit, 0)]:
                target = item.get("target") or {}
                print(f"- {item.get('path')}")
                print(f"  name: {item.get('name')}")
                print(f"  target: {target.get('project')} {target.get('repo')} {target.get('branch')}")
                print(f"  reason: {item.get('reason')}")
        if invalid:
            print("\nInvalid archive(s) ignored:")
            for item in invalid[: max(limit, 0)]:
                print(f"- {item.get('path')}")
                print(f"  reason: {item.get('reason')}")
        print("\nNext:")
        print(f"- validate a package: tul package check <package.zip> {ctx.project_id}")
        print(f"- use an explicit compatible package: tul update <package.zip>")
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
        warnings.append(f"{len(newer_incompatible) or len(incompatible)} incompatible package(s) ignored")
    if invalid:
        warnings.append(f"{len(invalid)} invalid archive(s) ignored")
    if warnings:
        print("\nWarnings:")
        for item in warnings:
            print(f"- {item}")
        print("Cleanup: tul clean packages")
    if latest_only:
        return
    print(f"\nMatching candidates shown: {min(limit, len(records))}/{len(records)}")
    for index, item in enumerate(records[: max(limit, 0)], start=1):
        marker = " selected" if index == 1 else ""
        target = item.get("target") or {}
        commit = item.get("commit") or {}
        print(f"[{index}]{marker} {item.get('name')}  {item.get('mtime')}")
        print(f"  path: {item.get('path')}")
        print(f"  target: {target.get('project')} {target.get('repo')} {target.get('branch')}")
        if commit.get("message"):
            print(f"  commit: {commit.get('message')}")


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
    print("# tul update dry")
    print("No repo files will be modified. This command imports, validates, and builds an apply plan only.")
    print()
    if package_path is None:
        print_package_candidates(ctx, limit=5, as_json=False, latest_only=True)
        print()
    print_import_plan(ctx, package_path=package_path)


def print_import_plan(ctx, *, package_path: str | None = None) -> None:
    branch = current_branch(ctx.repo_path)
    expected_branch = ctx.expected_branch or branch
    source = select_package(ctx.global_config, explicit=package_path, project=ctx.project_id, repo=ctx.expected_repo, branch=expected_branch)
    imported = import_package(source, ctx.global_config)
    state_file = imported.work_dir / "state.json"
    validate_manifest(imported.manifest, project=ctx.project_id, repo=ctx.expected_repo, branch=expected_branch)
    apply_plan = imported.work_dir / "apply-plan.json"
    planned = build_apply_plan(imported.manifest, extracted_dir=imported.extracted_dir, repo_path=ctx.repo_path, allowed_files=imported.manifest.commit_files)
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
    print("# tul package import plan")
    print(f"Project: {ctx.project_id}")
    print(f"Package: {source}")
    print(f"Work dir: {imported.work_dir}")
    print(f"State file: {state_file}")
    print(f"Apply plan: {apply_plan}")
    print(f"Planned operations: {len(planned)}")
    print("No repo files were modified.")
    print("To update, use: tul update")


# ----- launcher/setup helpers copied from prior CLI ------------------------------


def backup_path(path: Path) -> Path:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return path.with_name(f"{path.name}.bak-{stamp}")


def same_resolved(a: Path | None, b: Path | None) -> bool:
    if not a or not b:
        return False
    try:
        return a.resolve() == b.resolve()
    except Exception:
        return False


def launcher_version_label(path: Path, *, repo_bin: Path | None = None) -> str:
    if repo_bin is not None and same_resolved(path, repo_bin):
        return f"tul {__version__}"
    return "not checked (launcher is stale, copied, or outside target repo)"


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
                lines.append("- suggested fix: tul setup install " + str(repo))
        else:
            lines.append("- launcher status: missing")
            lines.append("- suggested fix: tul setup install " + str(repo))
    return lines


def install_launcher(repo: Path, *, copy: bool = False, force: bool = False) -> str:
    repo = repo.resolve()
    repo_launcher = repo / "bin" / "tul"
    if not repo_launcher.exists():
        raise TulError(f"missing repo launcher: {repo_launcher}")
    home_bin = Path.home() / "bin"
    home_bin.mkdir(parents=True, exist_ok=True)
    lines = ["# tul setup install", f"Repo: {repo}", f"Repo launcher: {repo_launcher}"]
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
