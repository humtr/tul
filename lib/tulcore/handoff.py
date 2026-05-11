from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from . import platform
from .gitops import branch, head, last_commit_files, recent, remote_url, status, upstream


@dataclass
class UpdateResult:
    mode: str = "initial-review"
    commit: str | None = None
    push_verified: bool | None = None
    rollback: str | None = None
    package: str | None = None


INVARIANTS = [
    "tul update pushes by default.",
    "--no-push is the exception.",
    "--no-commit is the exception.",
    "No git add -A.",
    "No force push.",
    "Rollback defaults to git revert + git push.",
    "Project-specific policy belongs in .tul.yml.",
    "Environment paths and aliases belong in global config.",
    "Windows and Termux package flow must converge.",
    "tul update prints handoff automatically after successful remote verification.",
]


def build(repo: Path, project: str | None, repo_config: dict, result: UpdateResult | None = None) -> str:
    result = result or UpdateResult()
    changed = last_commit_files(repo) if result.commit else []

    lines = [
        "# tul handoff",
        "",
        "## LLM instruction",
        "",
        "You are receiving a tul handoff.",
        "Treat it as a structured remote-review and next-package planning request.",
        "Verify the remote repo, branch, and expected HEAD when possible.",
        "If remote access is unavailable, say so explicitly.",
        "",
        "## Repository",
        "",
        f"Project: {project or repo.name}",
        f"Repo path: {repo}",
        f"Remote URL: {remote_url(repo) or '(none)'}",
        f"Configured repo: {repo_config.get('repo') or '(none)'}",
        f"Platform: {platform.name()}",
        f"Branch: {branch(repo)}",
        f"Expected branch: {repo_config.get('branch') or '(none)'}",
        f"HEAD: {head(repo)}",
        f"Upstream: {upstream(repo) or '(none)'}",
        "",
        "## Terminal verification",
        "",
        f"Mode: {result.mode}",
        f"Push verified: {result.push_verified if result.push_verified is not None else 'not available for this session'}",
        f"Commit: {result.commit or 'none'}",
        f"Package: {result.package or 'none'}",
        f"Working tree: {'clean' if not status(repo) else 'dirty'}",
    ]

    if result.rollback:
        lines.extend(["", "Rollback:", f"  {result.rollback}"])

    lines.extend(["", "## Recent commits", "", recent(repo), "", "## Changed files", ""])
    lines.extend(f"- {p}" for p in changed) if changed else lines.append("- none recorded for this handoff")

    lines.extend(["", "## Invariants", ""])
    lines.extend(f"- {x}" for x in INVARIANTS)

    lines.extend([
        "",
        "## Request to LLM",
        "",
        "1. Verify the remote repository, branch, and expected HEAD when possible.",
        "2. Read the latest relevant files from the remote repo.",
        "3. Separate user-stated goals, terminal-verified facts, assistant interpretation, and uncertainty.",
        "4. Identify structural debt, missing automation, and non-regression risks.",
        "5. Propose the next implementation package scope.",
        "6. Provide a short-term execution plan and long-term roadmap.",
        "7. If generating files, produce a cross-platform tul package with tul-package.yml and files/.",
        "8. Do not regress push-by-default semantics.",
        "",
    ])
    return "\n".join(lines)
