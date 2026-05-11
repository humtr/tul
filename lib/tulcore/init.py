"""Project onboarding for tul."""
from __future__ import annotations

from pathlib import Path

from .config import dump_yaml, load_global_config, load_repo_config, repo_config_path, save_global_config
from .gitops import clone, current_branch, remote_url, repo_root
from .paths import expand_path


def init_project(target: str, *, branch: str | None = None) -> tuple[Path, str]:
    global_config, global_path = load_global_config()
    projects = global_config.setdefault("projects", {})

    if "/" in target and not target.startswith((".", "~", "/")) and ":" not in target:
        project_id = target.split("/")[-1]
        existing = projects.get(project_id, {}) if isinstance(projects.get(project_id), dict) else {}
        repo_path = expand_path(existing.get("path") or f"~/prj/{project_id}")
        if not repo_path.exists():
            clone(target, repo_path)
        expected_repo = target
    else:
        repo_path = expand_path(target if _looks_like_path(target) else (projects.get(target, {}) or {}).get("path", f"~/prj/{target}"))
        project_id = repo_path.name if _looks_like_path(target) else target
        expected_repo = None

    repo_path = repo_root(repo_path)
    branch = branch or current_branch(repo_path)
    url = remote_url(repo_path)
    if not expected_repo and url:
        expected_repo = _slug_from_remote(url)

    projects[project_id] = {"path": str(repo_path)}
    save_global_config(global_config, global_path)

    repo_config = load_repo_config(repo_path)
    if not repo_config:
        repo_config = {
            "version": 1,
            "name": project_id,
            "repo": expected_repo or "unknown/unknown",
            "branch": branch,
            "track": "loop-runtime",
            "check": {"commands": ["python -m py_compile bin/tul", "python -m py_compile lib/tulcore/*.py", "git diff --check"]},
        }
        repo_config_path(repo_path).write_text(dump_yaml(repo_config) + "\n", encoding="utf-8", newline="\n")
    return repo_path, project_id


def _looks_like_path(target: str) -> bool:
    return any(sep in target for sep in ("/", "\\")) or target.startswith((".", "~")) or (len(target) > 1 and target[1] == ":")


def _slug_from_remote(url: str) -> str | None:
    text = url.strip()
    if text.endswith(".git"):
        text = text[:-4]
    if text.startswith("git@github.com:"):
        return text.split(":", 1)[1]
    if "github.com/" in text:
        return text.split("github.com/", 1)[1]
    return None
