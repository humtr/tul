"""Runtime project context helpers for native tul commands."""
from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .config import config_path, expand_path, load_global_config, resolve_project, save_global_config
from .errors import ConfigError
from .gitops import current_branch
from .paths import mkdirp


@dataclass
class InferredProject:
    ctx: Any
    reason: str
    warnings: list[str]


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


def _configured_project_ids() -> list[str]:
    config, _ = load_global_config()
    projects = config.get("projects") or {}
    return [str(key) for key, value in projects.items() if isinstance(value, dict) and value.get("path")]


def infer_project(target: str | None = None, *, command: str = "command", read_only: bool = True) -> InferredProject:
    """Infer a project for native/no-arg commands.

    Resolution order for omitted targets is:
    explicit target, current configured repo, active_project, default_project,
    single configured project. Mutating commands should use this helper only
    after adding their own conflict guard. v1b uses it for read-only commands.
    """
    warnings: list[str] = []
    if target:
        return InferredProject(resolve_project(target), "explicit target", warnings)

    cwd_match = project_for_cwd()
    active = active_project()
    default = default_project()

    if cwd_match:
        project_id, _ = cwd_match
        if active and active != project_id:
            warnings.append(
                "Context conflict: current directory project "
                f"{project_id!r} differs from active project {active!r}; "
                "using current directory project for this read-only command."
            )
        return InferredProject(resolve_project(project_id), "current directory project", warnings)

    if active:
        return InferredProject(resolve_project(active), "active_project", warnings)

    if default:
        return InferredProject(resolve_project(default), "default_project", warnings)

    project_ids = _configured_project_ids()
    if len(project_ids) == 1:
        return InferredProject(resolve_project(project_ids[0]), "only configured project", warnings)

    options = [
        f"tul use <project>",
        f"tul {command} <project>",
        "tul projects",
    ]
    if project_ids:
        options.append("configured projects: " + ", ".join(project_ids))
    raise ConfigError(
        "project target is ambiguous.\n"
        "Choose one of:\n- " + "\n- ".join(options)
    )



def infer_mutating_project(target: str | None = None, *, command: str = "command") -> InferredProject:
    """Infer a project for mutating/recovery commands with conflict guards.

    For explicit targets, this is the same as resolve_project(). For no-arg
    commands, a current-directory project is allowed only when it does not
    conflict with the stored active project. This prevents `tul update` from
    silently applying to a different repo than the one the user selected with
    `tul use`.
    """
    if target:
        return InferredProject(resolve_project(target), "explicit target", [])

    cwd_match = project_for_cwd()
    active = active_project()
    default = default_project()

    if cwd_match:
        project_id, repo = cwd_match
        if active and active != project_id:
            raise ConfigError(
                "context conflict for mutating command.\n\n"
                f"Active project: {active}\n"
                f"Current directory project: {project_id}\n"
                f"Current directory repo: {repo}\n\n"
                "Refusing no-arg command because the target is ambiguous.\n"
                "Choose one of:\n"
                f"- tul {command} {active}\n"
                f"- tul {command} {project_id}\n"
                f"- tul use {project_id}\n"
                f"- cd {resolve_project(active).repo_path if active else '<project-repo>'} && tul {command}"
            )
        return InferredProject(resolve_project(project_id), "current directory project", [])

    if active:
        return InferredProject(resolve_project(active), "active_project", [])

    if default:
        return InferredProject(resolve_project(default), "default_project", [])

    project_ids = _configured_project_ids()
    if len(project_ids) == 1:
        return InferredProject(resolve_project(project_ids[0]), "only configured project", [])

    options = [
        "tul use <project>",
        f"tul {command} <project>",
        "tul projects",
    ]
    if project_ids:
        options.append("configured projects: " + ", ".join(project_ids))
    raise ConfigError(
        "project target is ambiguous.\n"
        "Choose one of:\n- " + "\n- ".join(options)
    )


def format_inference_summary(inferred: InferredProject, *, command: str = "command") -> str:
    lines = ["# tul target"]
    lines.append(f"Command: {command}")
    lines.append(f"Project: {inferred.ctx.project_id}")
    lines.append(f"Repo: {inferred.ctx.repo_path}")
    lines.append(f"Reason: {inferred.reason}")
    return "\n".join(lines)


def format_inference_warnings(inferred: InferredProject) -> str:
    if not inferred.warnings:
        return ""
    return "\n".join(f"WARNING: {item}" for item in inferred.warnings)


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
        lines.append("- tul status")
        lines.append("- tul update")
        lines.append("- tul verify fresh")
    else:
        lines.append("- tul use <project>")
        lines.append("- tul init <project>")
    return "\n".join(lines)
