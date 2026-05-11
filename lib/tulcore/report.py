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
    if state_file:
        lines.append(f"State file: {state_file}")
    if commit_hash:
        lines.append(f"Commit: {commit_hash}")
    if push_verified is not None:
        lines.append(f"Push verified: {str(push_verified).lower()}")
    if rollback_command:
        lines.extend(["", "## Rollback", "", f"    {rollback_command}"])
    if changed_files:
        lines.extend(["", "## Changed files", ""])
        lines.extend(f"- {item}" for item in changed_files)
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
