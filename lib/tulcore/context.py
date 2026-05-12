"""Runtime project context helpers for native tul commands."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .config import config_path, expand_path, load_global_config, resolve_project, save_global_config
from .errors import ConfigError
from .gitops import current_branch
from .paths import mkdirp


def context_path() -> Path:
    """Return the runtime context file path next to the global config."""
    return config_path().with_name("context.json")


def load_context() -> dict[str, Any]:
    path = context_path()
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise ConfigError(f"could not read tul context file: {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ConfigError(f"tul context file must contain a JSON object: {path}")
    return data


def save_context(data: dict[str, Any]) -> Path:
    path = context_path()
    mkdirp(path.parent)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    return path


def set_active_project(project_id: str, *, repo_path: Path | None = None, set_by: str = "tul use") -> Path:
    data = load_context()
    data["active_project"] = project_id
    data["updated_at"] = datetime.now(timezone.utc).isoformat()
    data["set_by"] = set_by
    if repo_path is not None:
        data["repo_path"] = str(repo_path)
    return save_context(data)


def active_project() -> str | None:
    value = load_context().get("active_project")
    return str(value) if value else None


def set_default_project(project_id: str) -> Path:
    config, path = load_global_config()
    projects = config.get("projects") or {}
    if project_id not in projects:
        raise ConfigError(f"cannot set default_project to unknown project: {project_id}")
    config["default_project"] = project_id
    save_global_config(config, path)
    return path


def default_project() -> str | None:
    config, _ = load_global_config()
    value = config.get("default_project")
    return str(value) if value else None


def _is_relative_to(path: Path, base: Path) -> bool:
    try:
        path.resolve().relative_to(base.resolve())
        return True
    except Exception:
        return False


def project_for_cwd(cwd: Path | None = None) -> tuple[str, Path] | None:
    """Return the configured project containing cwd, preferring the deepest repo path."""
    config, _ = load_global_config()
    cwd = (cwd or Path.cwd()).resolve()
    matches: list[tuple[int, str, Path]] = []
    for project_id, value in (config.get("projects") or {}).items():
        if not isinstance(value, dict) or not value.get("path"):
            continue
        repo = expand_path(str(value["path"])).resolve()
        if cwd == repo or _is_relative_to(cwd, repo):
            matches.append((len(str(repo)), str(project_id), repo))
    if not matches:
        return None
    _, project_id, repo = sorted(matches, reverse=True)[0]
    return project_id, repo


def format_current_context() -> str:
    config, path = load_global_config()
    data = load_context()
    active = data.get("active_project") or None
    default = config.get("default_project") or None
    cwd_match = project_for_cwd()
    lines = ["# tul current"]
    lines.append(f"Config: {path}")
    lines.append(f"Context: {context_path()}")
    lines.append(f"Active project: {active or '(none)'}")
    lines.append(f"Default project: {default or '(none)'}")
    if cwd_match:
        lines.append(f"Current directory project: {cwd_match[0]}")
        lines.append(f"Current directory repo: {cwd_match[1]}")
    else:
        lines.append("Current directory project: (none)")
    if active:
        try:
            ctx = resolve_project(str(active))
            lines.append("Active project details:")
            lines.append(f"- repo: {ctx.repo_path}")
            lines.append(f"- branch: {current_branch(ctx.repo_path)}")
            if data.get("updated_at"):
                lines.append(f"- updated_at: {data.get('updated_at')}")
            if data.get("set_by"):
                lines.append(f"- set_by: {data.get('set_by')}")
        except Exception as exc:
            lines.append("Active project details:")
            lines.append(f"- error: {exc}")
    lines.append("Next:")
    if active or cwd_match or default:
        lines.append("- tul status <project>")
        lines.append("- tul update <project> -l")
        lines.append("- tul verify <project> --fresh-clone")
    else:
        lines.append("- tul use <project>")
        lines.append("- tul init <project>")
    return "\n".join(lines)
