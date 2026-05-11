from __future__ import annotations

from pathlib import Path

from . import platform
from .gitops import branch, compare_upstream, head, recent, remote_url, status, upstream


def status_text(repo: Path, project: str | None, repo_config: dict) -> str:
    lines = [
        f"repo     : {repo}",
        f"project  : {project or repo.name}",
    ]
    if repo_config.get("repo"):
        lines.append(f"config   : {repo_config.get('repo')}")
    lines.extend([
        f"branch   : {branch(repo)}",
        f"expected : {repo_config.get('branch') or '(none)'}",
        f"HEAD     : {head(repo, short=True)}",
        f"upstream : {upstream(repo) or '(none)'}",
    ])
    comp = compare_upstream(repo) if upstream(repo) else None
    if comp:
        lines.append(f"remote   : ahead {comp[0]}, behind {comp[1]}")
    st = status(repo)
    lines.append("status   : clean" if not st else "status   : dirty")
    lines.extend(f"  {x}" for x in st)
    return "\n".join(lines)


def report_text(repo: Path, project: str | None, repo_config: dict) -> str:
    return "\n".join([
        "# tul report",
        "",
        f"Repo: {repo}",
        f"Project: {project or repo.name}",
        f"Platform: {platform.name()}",
        f"Remote URL: {remote_url(repo) or '(none)'}",
        f"Branch: {branch(repo)}",
        f"Expected branch: {repo_config.get('branch') or '(none)'}",
        f"HEAD: {head(repo)}",
        f"Upstream: {upstream(repo) or '(none)'}",
        "",
        "Status:",
        *(f"  {x}" for x in (status(repo) or ["clean"])),
        "",
        "Recent commits:",
        recent(repo),
        "",
    ])
