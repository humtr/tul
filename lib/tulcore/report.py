"""Report generation."""
from __future__ import annotations

from pathlib import Path

from .gitops import current_branch, head, recent_commits, status_porcelain


def build_report(
    *,
    repo: Path,
    project: str,
    package_name: str | None = None,
    commit_hash: str | None = None,
    push_verified: bool | None = None,
    rollback_command: str | None = None,
    changed_files: list[str] | None = None,
    checks: list[str] | None = None,
    state_file: Path | None = None,
    outcome: str | None = None,
    apply_plan: Path | None = None,
    apply_log: Path | None = None,
    verify_fresh_ok: bool | None = None,
    verify_artifacts: dict[str, str] | None = None,
    repo_zip_export: dict[str, object] | None = None,
) -> str:
    lines = [
        "# tul update report",
        "",
        f"Project: {project}",
        f"Repo path: {repo}",
        f"Branch: {current_branch(repo)}",
        f"HEAD: {head(repo)}",
    ]
    if package_name:
        lines.append(f"Package: {package_name}")
    if outcome:
        lines.append(f"Outcome: {outcome}")
    if state_file:
        lines.append(f"State file: {state_file}")
    if apply_plan or apply_log:
        lines.extend(["", "## Apply artifacts", ""])
        if apply_plan:
            lines.append(f"- Apply plan: {apply_plan}")
        if apply_log:
            lines.append(f"- Apply log: {apply_log}")
    if commit_hash:
        lines.append(f"Commit: {commit_hash}")
    if outcome == "noop":
        lines.append("Push verified: not applicable for no-op")
    elif push_verified is not None:
        lines.append(f"Push verified: {str(push_verified).lower()}")
    if rollback_command:
        lines.extend(["", "## Rollback", "", f"    {rollback_command}"])
    if verify_fresh_ok is not None or verify_artifacts:
        lines.extend(["", "## Verify fresh", ""])
        if verify_fresh_ok is not None:
            lines.append(f"Release gate: {'PASS' if verify_fresh_ok else 'FAIL'}")
        if verify_artifacts:
            latest_md = verify_artifacts.get("latest_markdown")
            md = verify_artifacts.get("markdown")
            latest_json = verify_artifacts.get("latest_json")
            if latest_md:
                lines.append(f"- Latest markdown: {latest_md}")
            if md:
                lines.append(f"- Timestamped markdown: {md}")
            if latest_json:
                lines.append(f"- Latest JSON: {latest_json}")
    if repo_zip_export:
        lines.extend(["", "## Repo zip export", ""])
        if repo_zip_export.get("ok") is False:
            error = repo_zip_export.get("error") or repo_zip_export.get("error_type") or "failed"
            lines.append(f"- Result: failed ({error})")
        else:
            if repo_zip_export.get("path"):
                lines.append(f"- Path: {repo_zip_export['path']}")
            if repo_zip_export.get("sha256"):
                lines.append(f"- SHA256: {repo_zip_export['sha256']}")
            if repo_zip_export.get("size_bytes") is not None:
                lines.append(f"- Size bytes: {repo_zip_export['size_bytes']}")
            if repo_zip_export.get("file_count") is not None:
                lines.append(f"- Files: {repo_zip_export['file_count']}")
    if changed_files is not None:
        lines.extend(["", "## Changed files", ""])
        if changed_files:
            lines.extend(f"- {item}" for item in changed_files)
        else:
            lines.append("- none")
    if checks:
        lines.extend(["", "## Checks", ""])
        for item in checks:
            first = item.splitlines()[0] if item else "check"
            lines.append(f"- {first}")
    status = status_porcelain(repo)
    lines.extend(["", "## Working tree", "", "clean" if not status else status])
    lines.extend(["", "## Recent commits", ""])
    lines.extend(f"- {line}" for line in recent_commits(repo))
    return "\n".join(lines) + "\n"


def write_report(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")
