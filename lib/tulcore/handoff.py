"""LLM handoff prompt generation."""
from __future__ import annotations

from pathlib import Path

from .gitops import current_branch, fetch, head, recent_commits, remote_head, remote_url, status_porcelain


INVARIANTS = [
    "tul update pushes by default; --no-push is an exception.",
    "tul update is the full-loop command, not a split-command default.",
    "Never use git add -A or git add . in the default update path.",
    "Never force-push in the normal path.",
    "Project-specific policy belongs in .tul.yml, not engine code.",
    "Environment paths belong in global config, not engine code.",
    "Windows/Termux package flow should converge on tul-package.yml + files/.",
    "Successful update must print rollback instructions and an LLM-ready handoff.",
]


def generate_handoff(
    *,
    repo: Path,
    project: str,
    mode: str,
    expected_repo: str | None = None,
    package_name: str | None = None,
    commit_hash: str | None = None,
    push_verified: bool | None = None,
    changed_files: list[str] | None = None,
    validation: list[str] | None = None,
    rollback_command: str | None = None,
    state_file: Path | None = None,
    report_file: Path | None = None,
    outcome: str | None = None,
) -> str:
    branch = current_branch(repo)
    remote = None
    try:
        fetch(repo, branch)
        remote = remote_head(repo, branch)
    except Exception:
        remote = None
    status = status_porcelain(repo)
    lines = [
        "# tul LLM handoff",
        "",
        f"Mode: {mode}",
        f"Project: {project}",
        f"Repo path: {repo}",
        f"Repo URL: {remote_url(repo) or 'unknown'}",
        f"Expected repo: {expected_repo or 'unknown'}",
        f"Branch: {branch}",
        f"HEAD: {head(repo)}",
        f"Remote HEAD after fetch: {remote or 'unavailable'}",
        f"Working tree: {'clean' if not status else 'dirty'}",
    ]
    if package_name:
        lines.append(f"Active package: {package_name}")
    else:
        lines.append("Active package: none")
    if outcome:
        lines.append(f"Outcome: {outcome}")
    if commit_hash:
        lines.append(f"Commit hash: {commit_hash}")
    if push_verified is not None:
        lines.append(f"Push verified: {str(push_verified).lower()}")
    else:
        lines.append("Push verified: not available for this session")
    if state_file:
        lines.append(f"State file: {state_file}")
    if report_file:
        lines.append(f"Report file: {report_file}")
    if rollback_command:
        lines.extend(["", "## Rollback command", "", f"    {rollback_command}"])
    if changed_files:
        lines.extend(["", "## Changed files", ""])
        lines.extend(f"- {item}" for item in changed_files)
    if validation:
        lines.extend(["", "## Validation results", ""])
        for item in validation:
            lines.append(f"- {item.splitlines()[0] if item else 'check'}")
    lines.extend(["", "## Recent commits", ""])
    lines.extend(f"- {item}" for item in recent_commits(repo))
    lines.extend(["", "## Track / invariants", ""])
    lines.extend(f"- {item}" for item in INVARIANTS)
    lines.extend([
        "",
        "## Request to LLM",
        "",
        "1. Verify the remote repo, branch, and expected HEAD when remote access is available.",
        "2. If remote verification is unavailable, say so explicitly.",
        "3. Read the latest relevant repo files before proposing implementation.",
        "4. Compare terminal-verified facts against remote state.",
        "5. Check whether the invariants above were preserved.",
        "6. Identify remaining structural debt and missing automation.",
        "7. Propose the next package boundary and short/long roadmap.",
        "",
        "## Source separation",
        "",
        "사용자가 직접 말한 것:",
        "- tul은 Windows/Termux/LLM 사이의 폐루프 도구여야 한다.",
        "- tul update는 push, remote verification, rollback 안내, handoff 출력을 포함해야 한다.",
        "",
        "terminal-verified facts:",
        f"- Local HEAD at handoff generation: {head(repo)}",
        f"- Remote HEAD after fetch: {remote or 'unavailable'}",
        f"- Working tree status: {'clean' if not status else 'dirty'}",
        "",
        "assistant interpretation:",
        "- Treat this handoff as a structured remote-review request, not as proof that remote verification has already been done by the LLM.",
        "",
        "불확실하거나 확인 필요한 부분:",
        "- Remote file contents must be re-read by the receiving LLM if repository access is available.",
    ])
    return "\n".join(lines) + "\n"
