"""Configuration loading and a small YAML subset parser/writer."""
from __future__ import annotations

import copy
import re
from datetime import datetime
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .errors import ConfigError
from .paths import expand_path, mkdirp
from .platform import default_config_path, default_global_config


@dataclass
class ProjectContext:
    target: str
    project_id: str
    repo_path: Path
    global_config: dict[str, Any]
    repo_config: dict[str, Any]
    global_config_path: Path

    @property
    def name(self) -> str:
        return str(self.repo_config.get("name") or self.project_id)

    @property
    def expected_repo(self) -> str | None:
        value = self.repo_config.get("repo")
        return str(value) if value else None

    @property
    def expected_branch(self) -> str | None:
        value = self.repo_config.get("branch")
        return str(value) if value else None


def _strip_comment(line: str) -> str:
    in_single = False
    in_double = False
    out = []
    for ch in line:
        if ch == "'" and not in_double:
            in_single = not in_single
        elif ch == '"' and not in_single:
            in_double = not in_double
        elif ch == "#" and not in_single and not in_double:
            break
        out.append(ch)
    return "".join(out).rstrip()


def _parse_scalar(text: str) -> Any:
    text = text.strip()
    if text == "":
        return ""
    if text in {"null", "Null", "NULL", "~"}:
        return None
    if text in {"true", "True", "TRUE"}:
        return True
    if text in {"false", "False", "FALSE"}:
        return False
    if (text.startswith('"') and text.endswith('"')) or (text.startswith("'") and text.endswith("'")):
        return text[1:-1]
    if re.fullmatch(r"-?\d+", text):
        try:
            return int(text)
        except ValueError:
            pass
    if re.fullmatch(r"-?\d+\.\d+", text):
        try:
            return float(text)
        except ValueError:
            pass
    return text


def _preprocess_yaml(text: str) -> list[tuple[int, str]]:
    result: list[tuple[int, str]] = []
    for raw in text.splitlines():
        stripped_comment = _strip_comment(raw)
        if stripped_comment.strip() == "":
            continue
        indent = len(stripped_comment) - len(stripped_comment.lstrip(" "))
        if "\t" in stripped_comment[:indent]:
            raise ConfigError("tabs are not supported in YAML indentation")
        result.append((indent, stripped_comment.strip()))
    return result


def _parse_block(lines: list[tuple[int, str]], index: int, indent: int) -> tuple[Any, int]:
    if index >= len(lines):
        return {}, index
    first_indent, first_text = lines[index]
    if first_indent < indent:
        return {}, index
    is_list = first_text.startswith("- ")
    if is_list:
        items: list[Any] = []
        while index < len(lines):
            current_indent, text = lines[index]
            if current_indent < indent:
                break
            if current_indent > indent:
                raise ConfigError(f"unexpected indentation near: {text}")
            if not text.startswith("- "):
                break
            item_text = text[2:].strip()
            index += 1
            if item_text == "":
                child, index = _parse_block(lines, index, indent + 2)
                items.append(child)
            elif ":" in item_text and not item_text.startswith(("'", '"')):
                key, value = item_text.split(":", 1)
                item: dict[str, Any] = {}
                key = key.strip()
                value = value.strip()
                if value:
                    item[key] = _parse_scalar(value)
                else:
                    child, index = _parse_block(lines, index, indent + 2)
                    item[key] = child
                while index < len(lines):
                    next_indent, next_text = lines[index]
                    if next_indent < indent + 2:
                        break
                    if next_indent != indent + 2 or next_text.startswith("- "):
                        break
                    extra_key, extra_value = next_text.split(":", 1)
                    extra_key = extra_key.strip()
                    extra_value = extra_value.strip()
                    index += 1
                    if extra_value:
                        item[extra_key] = _parse_scalar(extra_value)
                    else:
                        child, index = _parse_block(lines, index, indent + 4)
                        item[extra_key] = child
                items.append(item)
            else:
                items.append(_parse_scalar(item_text))
        return items, index

    mapping: dict[str, Any] = {}
    while index < len(lines):
        current_indent, text = lines[index]
        if current_indent < indent:
            break
        if current_indent > indent:
            raise ConfigError(f"unexpected indentation near: {text}")
        if text.startswith("- "):
            break
        if ":" not in text:
            raise ConfigError(f"expected key/value line near: {text}")
        key, value = text.split(":", 1)
        key = key.strip()
        value = value.strip()
        index += 1
        if value:
            mapping[key] = _parse_scalar(value)
        else:
            child, index = _parse_block(lines, index, indent + 2)
            mapping[key] = child
    return mapping, index


def load_yaml_text(text: str) -> dict[str, Any]:
    try:
        import yaml  # type: ignore
    except Exception:
        yaml = None
    if yaml is not None:
        data = yaml.safe_load(text) or {}
        if not isinstance(data, dict):
            raise ConfigError("YAML document must be a mapping")
        return data
    lines = _preprocess_yaml(text)
    if not lines:
        return {}
    data, index = _parse_block(lines, 0, lines[0][0])
    if index != len(lines):
        raise ConfigError("could not parse full YAML document")
    if not isinstance(data, dict):
        raise ConfigError("YAML document must be a mapping")
    return data


def load_yaml_file(path: Path, *, required: bool = False) -> dict[str, Any]:
    if not path.exists():
        if required:
            raise ConfigError(f"missing config file: {path}")
        return {}
    return load_yaml_text(path.read_text(encoding="utf-8"))


def dump_yaml(data: Any, indent: int = 0) -> str:
    pad = " " * indent
    if isinstance(data, dict):
        lines = []
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                lines.append(f"{pad}{key}:")
                lines.append(dump_yaml(value, indent + 2))
            else:
                lines.append(f"{pad}{key}: {_format_scalar(value)}")
        return "\n".join(lines)
    if isinstance(data, list):
        lines = []
        for item in data:
            if isinstance(item, dict):
                if not item:
                    lines.append(f"{pad}- {{}}")
                    continue
                first = True
                for key, value in item.items():
                    prefix = "- " if first else "  "
                    if isinstance(value, (dict, list)):
                        lines.append(f"{pad}{prefix}{key}:")
                        lines.append(dump_yaml(value, indent + 4))
                    else:
                        lines.append(f"{pad}{prefix}{key}: {_format_scalar(value)}")
                    first = False
            elif isinstance(item, (dict, list)):
                lines.append(f"{pad}-")
                lines.append(dump_yaml(item, indent + 2))
            else:
                lines.append(f"{pad}- {_format_scalar(item)}")
        return "\n".join(lines)
    return f"{pad}{_format_scalar(data)}"


def _format_scalar(value: Any) -> str:
    if value is True:
        return "true"
    if value is False:
        return "false"
    if value is None:
        return "null"
    text = str(value)
    if text == "" or text.startswith((" ", "@", "`", "-", "?", ":", "{", "[", "#", "&", "*", "!", "|", ">", "'", '"')) or ": " in text:
        return '"' + text.replace('"', '\\"') + '"'
    return text


def config_path() -> Path:
    return default_config_path()


def load_global_config() -> tuple[dict[str, Any], Path]:
    path = config_path()
    config = copy.deepcopy(default_global_config())
    if path.exists():
        loaded = load_yaml_file(path)
        config = _deep_merge(config, loaded)
    config.setdefault("projects", {})
    config.setdefault("platform", {})
    return config, path


def save_global_config(config: dict[str, Any], path: Path | None = None) -> None:
    path = path or config_path()
    mkdirp(path.parent)
    if path.exists():
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup = path.with_name(f"{path.name}.bak-{stamp}")
        backup.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
    path.write_text(dump_yaml(config) + "\n", encoding="utf-8", newline="\n")


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def repo_config_path(repo_path: Path) -> Path:
    return repo_path / ".tul.yml"


def load_repo_config(repo_path: Path) -> dict[str, Any]:
    return load_yaml_file(repo_config_path(repo_path))


def looks_like_path(target: str) -> bool:
    return any(sep in target for sep in ("/", "\\")) or target.startswith((".", "~")) or (len(target) > 1 and target[1] == ":")


def resolve_project(target: str) -> ProjectContext:
    global_config, global_path = load_global_config()
    projects = global_config.get("projects") or {}
    if target in projects and isinstance(projects[target], dict) and projects[target].get("path"):
        repo_path = expand_path(str(projects[target]["path"]))
        project_id = target
    elif looks_like_path(target):
        repo_path = expand_path(target)
        project_id = repo_path.name
    else:
        raise ConfigError(
            f"unknown project alias: {target}\n"
            f"Run 'tul setup init {target}' or add it to {global_path}."
        )
    repo_path = repo_path.resolve()
    repo_config = load_repo_config(repo_path)
    if not repo_config:
        repo_config = {"version": 1, "name": project_id}
    project_id = str(repo_config.get("name") or project_id)
    return ProjectContext(
        target=target,
        project_id=project_id,
        repo_path=repo_path,
        global_config=global_config,
        repo_config=repo_config,
        global_config_path=global_path,
    )


def platform_paths(config: dict[str, Any]) -> dict[str, Any]:
    platform = config.get("platform") or {}
    result = dict(platform)
    for key in ("work_root", "archive_root", "backup_root", "log_root", "verify_log_root"):
        if result.get(key):
            result[key] = expand_path(str(result[key]))
    roots = []
    for raw in result.get("inbox_roots") or []:
        roots.append(expand_path(str(raw)))
    result["inbox_roots"] = roots
    return result
