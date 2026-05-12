"""Full update pipeline orchestration."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .apply import apply_copy
from .checks import run_checks
from .config import ProjectContext
from .handoff import generate_handoff
from .manifest import validate_manifest
from .package import import_package, select_package
from .precheck import run_precheck
from .publish import publish_manifest_changes
from .report import build_report, write_report
from .state import record_error, set_phase
from .sweep import sweep_repo
from .verify import format_verify_gate, run_verify, write_verify_artifacts


@dataclass
class UpdateResult:
    report: str
    handoff: str
    work_dir: Path
    commit_hash: str | None
    push_verified: bool
    state_file: Path
    verify_ok: bool | None = None
    verify_text: str | None = None
    verify_artifacts: dict[str, str] | None = None


def run_update(
    ctx: ProjectContext,
    *,
    package_path: str | None = None,
    no_commit: bool = False,
    no_push: bool = False,
    allow_dirty: bool = False,
    verify_after: bool = True,
) -> UpdateResult:
    repo = ctx.repo_path
    state_file: Path | None = None
    failed_at = "precheck"
    try:
        precheck = run_precheck(ctx, allow_dirty=allow_dirty)
        branch = precheck.branch
        expected_branch = ctx.expected_branch or branch

        failed_at = "package-select"
        source = select_package(
            ctx.global_config,
            explicit=package_path,
            project=ctx.project_id,
            repo=ctx.expected_repo,
            branch=expected_branch,
        )

        failed_at = "import"
        imported = import_package(source, ctx.global_config)
        state_file = imported.work_dir / "state.json"
        set_phase(
            state_file,
            "imported",
            project=ctx.project_id,
            repo=str(repo),
            branch=branch,
            package=str(source),
            package_name=imported.manifest.name,
            sha256=imported.sha256,
            precheck={
                "dirty": precheck.dirty,
                "ahead": precheck.ahead,
                "behind": precheck.behind,
                "pulled": precheck.pulled,
            },
        )

        failed_at = "manifest-validation"
        validate_manifest(imported.manifest, project=ctx.project_id, repo=ctx.expected_repo, branch=expected_branch)
        set_phase(state_file, "validated", manifest=imported.manifest.data)

        failed_at = "apply"
        backup_dir = imported.work_dir / "backups"
        apply_log = imported.work_dir / "apply.log"
        apply_plan = imported.work_dir / "apply-plan.json"
        applied_files = apply_copy(
            imported.manifest,
            extracted_dir=imported.extracted_dir,
            repo_path=repo,
            backup_dir=backup_dir,
            log_path=apply_log,
            plan_path=apply_plan,
            allowed_files=imported.manifest.commit_files,
        )
        set_phase(
            state_file,
            "applied",
            applied_files=applied_files,
            apply_log=str(apply_log),
            apply_plan=str(apply_plan),
        )

        failed_at = "checks"
        checks = run_checks(repo, ctx.repo_config, log_path=imported.work_dir / "check.log")
        set_phase(state_file, "checked", checks_count=len(checks))

        failed_at = "sweep"
        moved = sweep_repo(repo, ctx.global_config)
        set_phase(state_file, "swept", swept=moved)

        failed_at = "publish"
        publish = publish_manifest_changes(
            repo=repo,
            branch=branch,
            files=imported.manifest.commit_files,
            message=imported.manifest.commit_message,
            no_commit=no_commit,
            no_push=no_push,
            state_file=state_file,
        )

        push_value = publish.push_verified if publish.commit_hash and not no_push else None
        visible_changed_files = publish.changed_files or publish.staged_files

        verify_result = None
        verify_artifacts = None
        verify_text = None
        # In the normal full-loop path, include a fresh verification gate after
        # publish/no-op handling so the terminal output and uploaded artifact both
        # represent the final HEAD that the LLM should inspect next. Debug paths
        # that intentionally skip commit or push would often make fresh remote
        # verification misleading, so they do not run this automatic gate.
        if verify_after and not no_commit and not no_push:
            failed_at = "verify-fresh"
            verify_result = run_verify(ctx, fresh_clone=True)
            verify_artifacts = write_verify_artifacts(ctx, verify_result, fresh_clone=True)
            verify_text = format_verify_gate(verify_result, verify_artifacts)

        report = build_report(
            repo=repo,
            project=ctx.project_id,
            package_name=imported.manifest.name,
            commit_hash=publish.commit_hash,
            push_verified=push_value,
            rollback_command=publish.rollback_command,
            changed_files=visible_changed_files,
            checks=checks,
            state_file=state_file,
            outcome=publish.outcome,
            apply_plan=apply_plan,
            apply_log=apply_log,
            verify_fresh_ok=verify_result.ok if verify_result is not None else None,
            verify_artifacts=verify_artifacts,
        )
        report_path = imported.work_dir / "report.md"
        write_report(report_path, report)

        if publish.no_op:
            handoff_mode = "update-noop"
        elif publish.commit_hash:
            handoff_mode = "post-update"
        else:
            handoff_mode = "update-no-commit"
        handoff = generate_handoff(
            repo=repo,
            project=ctx.project_id,
            mode=handoff_mode,
            expected_repo=ctx.expected_repo,
            package_name=imported.manifest.name,
            commit_hash=publish.commit_hash,
            push_verified=push_value,
            changed_files=visible_changed_files,
            validation=checks,
            rollback_command=publish.rollback_command,
            state_file=state_file,
            report_file=report_path,
            outcome=publish.outcome,
            verify_fresh_ok=verify_result.ok if verify_result is not None else None,
            verify_artifacts=verify_artifacts,
        )
        handoff_path = imported.work_dir / "handoff.md"
        handoff_path.write_text(handoff, encoding="utf-8", newline="\n")
        set_phase(
            state_file,
            "handoff-ready",
            report=str(report_path),
            handoff=str(handoff_path),
            commit=publish.commit_hash,
            push_verified=push_value,
            outcome=publish.outcome,
            no_op=publish.no_op,
            changed_files=visible_changed_files,
            verify_fresh_ok=verify_result.ok if verify_result is not None else None,
            verify_artifacts=verify_artifacts,
        )
        return UpdateResult(
            report=report,
            handoff=handoff,
            work_dir=imported.work_dir,
            commit_hash=publish.commit_hash,
            push_verified=publish.push_verified,
            state_file=state_file,
            verify_ok=verify_result.ok if verify_result is not None else None,
            verify_text=verify_text,
            verify_artifacts=verify_artifacts,
        )
    except Exception as exc:
        record_error(state_file, exc, failed_at=failed_at)
        raise
