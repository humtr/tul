"""Project onboarding for tul."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .config import dump_yaml, load_global_config, load_repo_config, repo_config_path, save_global_config
from .errors import ConfigError, GitError
from .gitops import ahead_behind, clone, current_branch, fetch, is_dirty, pull_ff_only, remote_url, repo_root
from .paths import expand_path, mkdirp


DEFAULT_CHECK_COMMANDS = [
    "python -m py_compile bin/tul",
    "python -m py_compile lib/tulcore/*.py",
    "git diff --check",
]


@dataclass
class InitResult:
    repo_path: Path
    project_id: str
    expected_repo: str | None
    branch: str
    global_config_path: Path
    repo_config_path: Path
    actions: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def summary(self) -> str:
        lines = ["# tul setup init", f"Project: {self.project_id}", f"Repo: {self.repo_path}"]
        if self.expected_repo:
            lines.append(f"Expected repo: {self.expected_repo}")
        lines.append(f"Branch: {self.branch}")
        lines.append(f"Global config: {self.global_config_path}")
        lines.append(f"Repo config: {self.repo_config_path}")
        if self.actions:
            lines.append("\nActions:")
            lines.extend(f"- {item}" for item in self.actions)
        if self.warnings:
            lines.append("\nWarnings:")
            lines.extend(f"- {item}" for item in self.warnings)
        lines.append("\nNext:")
        lines.append(f"- tul show {self.project_id}")
        lines.append(f"- tul run {self.project_id}")
        lines.append(f"- tul show handoff {self.project_id}")
        return "\n".join(lines)


def init_project(target: str, *, branch: str | None = None, project: str | None = None) -> InitResult:
    """Register or repair tul onboarding for a repo.

    The command is intentionally conservative: it may create or fill missing
    config keys, but it does not delete existing config values and it does not
    switch branches or merge/rebase.
    """
    global_config, global_path = load_global_config()
    projects = global_config.setdefault("projects", {})
    actions: list[str] = []
    warnings: list[str] = []

    repo_path, project_id, expected_repo = _resolve_init_target(target, projects, project=project)
    if not repo_path.exists():
        if not expected_repo:
            raise ConfigError(f"repo path does not exist and target is not a GitHub slug: {repo_path}")
        clone(expected_repo, repo_path)
        actions.append(f"cloned {expected_repo} to {repo_path}")

    repo_path = repo_root(repo_path)
    current = current_branch(repo_path)
    expected_branch = branch or current
    url = remote_url(repo_path)
    remote_slug = _slug_from_remote(url or "")
    expected_repo = expected_repo or remote_slug

    if branch and current != branch:
        warnings.append(f"current branch is {current}, expected branch is {branch}; init does not switch branches")

    if is_dirty(repo_path):
        warnings.append("working tree is dirty; init will not pull")
    else:
        try:
            fetch(repo_path, current)
            ab = ahead_behind(repo_path, current)
            if ab:
                ahead, behind = ab
                if behind and not ahead:
                    pull_ff_only(repo_path)
                    actions.append("pulled --ff-only")
                elif behind and ahead:
                    warnings.append(f"branch is diverged from origin/{current}; init did not pull")
        except GitError as exc:
            warnings.append(f"fetch/pull skipped: {exc}")

    # Prefer explicit project, then existing .tul.yml name, then slug/path name.
    repo_config = load_repo_config(repo_path)
    if not project:
        project_id = str(repo_config.get("name") or project_id)

    existing_project = projects.get(project_id)
    desired_path = _display_path(repo_path)
    if not isinstance(existing_project, dict) or existing_project.get("path") != desired_path:
        projects[project_id] = {"path": desired_path}
        actions.append(f"registered project alias {project_id}: {desired_path}")
    else:
        actions.append(f"project alias {project_id} already registered")
    save_global_config(global_config, global_path)

    repo_config_path_value = repo_config_path(repo_path)
    new_repo_config, changed = _merge_repo_config(
        repo_config,
        project_id=project_id,
        expected_repo=expected_repo,
        branch=expected_branch,
    )
    if changed or not repo_config_path_value.exists():
        if repo_config_path_value.exists():
            backup = repo_config_path_value.with_name(f".tul.yml.bak-{_stamp()}")
            backup.write_text(repo_config_path_value.read_text(encoding="utf-8"), encoding="utf-8")
            actions.append(f"backed up .tul.yml to {backup.name}")
        repo_config_path_value.write_text(dump_yaml(new_repo_config) + "\n", encoding="utf-8", newline="\n")
        actions.append("created/updated .tul.yml")
    else:
        actions.append(".tul.yml already complete")

    # Create the active status directory without recreating retired documentation
    # namespaces. Do not overwrite existing docs.
    for rel in ("docs/status",):
        path = repo_path / rel
        if not path.exists():
            mkdirp(path)
            actions.append(f"created {rel}/")

    return InitResult(
        repo_path=repo_path,
        project_id=project_id,
        expected_repo=expected_repo,
        branch=expected_branch,
        global_config_path=global_path,
        repo_config_path=repo_config_path_value,
        actions=actions,
        warnings=warnings,
    )


def _resolve_init_target(target: str, projects: dict[str, Any], *, project: str | None = None) -> tuple[Path, str, str | None]:
    if _is_github_slug(target):
        project_id = project or target.split("/")[-1]
        existing = projects.get(project_id, {}) if isinstance(projects.get(project_id), dict) else {}
        return expand_path(existing.get("path") or f"~/prj/{project_id}"), project_id, target

    if _looks_like_path(target):
        repo_path = expand_path(target)
        return repo_path, project or repo_path.name, None

    # Alias or bare project id.
    existing = projects.get(target, {}) if isinstance(projects.get(target), dict) else {}
    repo_path = expand_path(existing.get("path") or f"~/prj/{target}")
    return repo_path, project or target, None


def _merge_repo_config(repo_config: dict[str, Any], *, project_id: str, expected_repo: str | None, branch: str) -> tuple[dict[str, Any], bool]:
    config = dict(repo_config or {})
    changed = False
    defaults = {
        "version": 1,
        "name": project_id,
        "repo": expected_repo or "unknown/unknown",
        "branch": branch,
        "track": "loop-runtime",
    }
    for key, value in defaults.items():
        if not config.get(key):
            config[key] = value
            changed = True
    check = config.get("check")
    if not isinstance(check, dict):
        config["check"] = {"commands": DEFAULT_CHECK_COMMANDS[:]}
        changed = True
    else:
        commands = check.get("commands")
        if not isinstance(commands, list) or not commands:
            check["commands"] = DEFAULT_CHECK_COMMANDS[:]
            changed = True
    return config, changed


def _looks_like_path(target: str) -> bool:
    return any(sep in target for sep in ("/", "\\")) or target.startswith((".", "~")) or (len(target) > 1 and target[1] == ":")


def _is_github_slug(target: str) -> bool:
    return "/" in target and not target.startswith((".", "~", "/")) and ":" not in target and not target.lower().startswith(("http://", "https://"))


def _slug_from_remote(url: str) -> str | None:
    text = url.strip()
    if text.endswith(".git"):
        text = text[:-4]
    if text.startswith("git@github.com:"):
        return text.split(":", 1)[1]
    if "github.com/" in text:
        return text.split("github.com/", 1)[1]
    return None


def _display_path(path: Path) -> str:
    try:
        home = Path.home().resolve()
        resolved = path.resolve()
        rel = resolved.relative_to(home)
        return "~/" + rel.as_posix()
    except Exception:
        return str(path)


def _stamp() -> str:
    from datetime import datetime
    return datetime.now().strftime("%Y%m%d-%H%M%S")
