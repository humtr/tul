from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .errors import TulError
from .simpleyaml import parse


@dataclass
class Manifest:
    path: Path
    data: dict[str, Any]

    @property
    def name(self) -> str:
        return str(self.data.get("name") or "unnamed")

    @property
    def target(self) -> dict[str, Any]:
        return self.data.get("target") or {}

    @property
    def apply(self) -> dict[str, Any]:
        return self.data.get("apply") or {}

    @property
    def commit(self) -> dict[str, Any]:
        return self.data.get("commit") or {}

    def target_project(self) -> str | None:
        return str(self.target.get("project")) if self.target.get("project") else None

    def target_repo(self) -> str | None:
        return str(self.target.get("repo")) if self.target.get("repo") else None

    def target_branch(self) -> str | None:
        return str(self.target.get("branch")) if self.target.get("branch") else None

    def mode(self) -> str:
        return str(self.apply.get("mode") or "copy")

    def apply_files(self) -> list[dict[str, str]]:
        raw = self.apply.get("files") or []
        if not isinstance(raw, list):
            raise TulError("apply.files must be a list")
        out = []
        for item in raw:
            if not isinstance(item, dict) or not item.get("from") or not item.get("to"):
                raise TulError("apply.files entries require from/to")
            out.append({"from": str(item["from"]), "to": str(item["to"])})
        return out

    def commit_files(self) -> list[str]:
        raw = self.commit.get("files") or []
        if not isinstance(raw, list) or not raw:
            raise TulError("commit.files must be a non-empty list")
        return [str(x).replace("\\", "/") for x in raw]

    def message(self) -> str:
        msg = self.commit.get("message")
        if not msg:
            raise TulError("commit.message is required")
        return str(msg)


def load(path: Path) -> Manifest:
    data = parse(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise TulError(f"invalid manifest: {path}")
    return Manifest(path, data)


def find(root: Path) -> Path | None:
    direct = root / "tul-package.yml"
    if direct.exists():
        return direct
    found = sorted(root.rglob("tul-package.yml"))
    return found[0] if found else None


def validate(m: Manifest, project: str | None, repo_slug: str | None, branch: str) -> None:
    if m.target_project() and project and m.target_project() != project:
        raise TulError(f"target.project mismatch: {m.target_project()} != {project}")
    if m.target_repo() and repo_slug and m.target_repo() != repo_slug:
        raise TulError(f"target.repo mismatch: {m.target_repo()} != {repo_slug}")
    if m.target_branch() and m.target_branch() != branch:
        raise TulError(f"target.branch mismatch: {m.target_branch()} != {branch}")
    if m.mode() != "copy":
        raise TulError(f"unsupported apply.mode: {m.mode()}")
    if not m.apply_files():
        raise TulError("apply.files is empty")
    m.commit_files()
    m.message()
