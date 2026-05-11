"""Package manifest validation."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .config import load_yaml_file
from .errors import ManifestError
from .paths import normalize_repo_relative


@dataclass
class Manifest:
    path: Path
    data: dict[str, Any]

    @property
    def name(self) -> str:
        return str(self.data.get("name") or self.path.parent.name)

    @property
    def target(self) -> dict[str, Any]:
        return self.data.get("target") or {}

    @property
    def apply(self) -> dict[str, Any]:
        return self.data.get("apply") or {}

    @property
    def commit(self) -> dict[str, Any]:
        return self.data.get("commit") or {}

    @property
    def commit_files(self) -> list[str]:
        files = self.commit.get("files") or []
        if not isinstance(files, list) or not files:
            raise ManifestError("commit.files must be a non-empty list")
        return [normalize_repo_relative(str(item)) for item in files]

    @property
    def commit_message(self) -> str:
        message = str(self.commit.get("message") or "").strip()
        if not message:
            raise ManifestError("commit.message is required")
        return message


def load_manifest(path: Path) -> Manifest:
    if path.is_dir():
        path = path / "tul-package.yml"
    data = load_yaml_file(path, required=True)
    return Manifest(path=path, data=data)


def validate_manifest(manifest: Manifest, *, project: str, repo: str | None, branch: str | None) -> None:
    data = manifest.data
    if int(data.get("version") or 0) != 1:
        raise ManifestError("manifest version must be 1")
    target = manifest.target
    for key in ("project", "repo", "branch"):
        if not target.get(key):
            raise ManifestError(f"target.{key} is required")
    if str(target.get("project")) != str(project):
        raise ManifestError(f"target.project mismatch: expected {project}, got {target.get('project')}")
    if repo and str(target.get("repo")) != str(repo):
        raise ManifestError(f"target.repo mismatch: expected {repo}, got {target.get('repo')}")
    if branch and str(target.get("branch")) != str(branch):
        raise ManifestError(f"target.branch mismatch: expected {branch}, got {target.get('branch')}")
    apply = manifest.apply
    if apply.get("mode") != "copy":
        raise ManifestError("only apply.mode: copy is supported")
    files = apply.get("files")
    if not isinstance(files, list) or not files:
        raise ManifestError("apply.files must be a non-empty list")
    for index, item in enumerate(files):
        if not isinstance(item, dict):
            raise ManifestError(f"apply.files[{index}] must be a mapping")
        if not item.get("from") or not item.get("to"):
            raise ManifestError(f"apply.files[{index}] requires from and to")
        normalize_repo_relative(str(item["from"]))
        normalize_repo_relative(str(item["to"]))
    manifest.commit_files
    manifest.commit_message
