from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from . import platform
from .simpleyaml import parse, dump


@dataclass
class GlobalConfig:
    path: Path
    data: dict[str, Any]

    @property
    def projects(self) -> dict[str, Any]:
        return self.data.setdefault("projects", {})

    @property
    def platform(self) -> dict[str, Any]:
        return self.data.setdefault("platform", {})

    def inbox_roots(self) -> list[Path]:
        values = self.platform.get("inbox_roots") or []
        if not values:
            return platform.default_inbox_roots()
        return [Path(str(v)).expanduser() for v in values]

    def work_root(self) -> Path:
        return Path(str(self.platform.get("work_root") or platform.default_work_root())).expanduser()

    def archive_root(self) -> Path:
        return Path(str(self.platform.get("archive_root") or platform.default_archive_root())).expanduser()

    def backup_root(self) -> Path:
        return Path(str(self.platform.get("backup_root") or platform.default_backup_root())).expanduser()


def default_config_data() -> dict[str, Any]:
    return {
        "version": 1,
        "platform": {
            "inbox_roots": [str(p) for p in platform.default_inbox_roots()],
            "work_root": str(platform.default_work_root()),
            "archive_root": str(platform.default_archive_root()),
            "backup_root": str(platform.default_backup_root()),
            "clipboard_command": platform.default_clipboard_command() or "",
        },
        "projects": {},
    }


def load_global(create: bool = False) -> GlobalConfig:
    path = platform.config_path()
    if not path.exists():
        cfg = GlobalConfig(path, default_config_data())
        if create:
            save_global(cfg)
        return cfg
    data = parse(path.read_text(encoding="utf-8"))
    return GlobalConfig(path, data if isinstance(data, dict) else default_config_data())


def save_global(cfg: GlobalConfig) -> None:
    cfg.path.parent.mkdir(parents=True, exist_ok=True)
    cfg.path.write_text(dump(cfg.data), encoding="utf-8", newline="\n")


def load_repo(repo: Path) -> dict[str, Any]:
    path = repo / ".tul.yml"
    if not path.exists():
        return {}
    data = parse(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def save_repo(repo: Path, data: dict[str, Any]) -> None:
    (repo / ".tul.yml").write_text(dump(data), encoding="utf-8", newline="\n")


def repo_name_from_slug(slug: str) -> str:
    return slug.rstrip("/").split("/")[-1].removesuffix(".git")


def slug_from_remote(url: str) -> str:
    text = url.strip()
    if text.endswith(".git"):
        text = text[:-4]
    if "@" in text and ":" in text and not text.startswith("http"):
        return text.split(":", 1)[1]
    if "github.com/" in text:
        return text.split("github.com/", 1)[1]
    return text
