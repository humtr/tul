"""Upload-friendly head-tagged artifact helpers.

The human-facing import root is an upload surface, not a historical archive.
It should show only the current commit-tagged source/review/verify artifacts.
Dated archival copies remain under logs/<kind>/YYMMDD.
"""
from __future__ import annotations

import re
import shutil
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from .config import ProjectContext, platform_paths
from .gitops import head as git_head
from .paths import mkdirp


@dataclass
class UploadAliasResult:
    kind: str
    head: str
    root_alias: str | None = None
    dated_alias: str | None = None
    dated_json_alias: str | None = None
    removed_root_aliases: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "kind": self.kind,
            "head": self.head,
        }
        if self.root_alias:
            payload["root_alias"] = self.root_alias
        if self.dated_alias:
            payload["dated_alias"] = self.dated_alias
        if self.dated_json_alias:
            payload["dated_json_alias"] = self.dated_json_alias
        if self.removed_root_aliases:
            payload["removed_root_aliases"] = list(self.removed_root_aliases)
        return payload


def import_root(ctx: ProjectContext) -> Path:
    """Return the human-facing import/upload root for a project."""
    paths = platform_paths(ctx.global_config)
    work_root = paths.get("work_root")
    if work_root:
        return Path(work_root).parent
    return ctx.repo_path.parent


def head_alias_path(ctx: ProjectContext, *, kind: str, suffix: str, head: str | None = None) -> Path:
    """Return the canonical human-upload root alias for a kind and HEAD."""
    full_head = _head(ctx, head)
    return import_root(ctx) / f"{ctx.project_id}-{kind}-{full_head[:7]}{suffix}"


def remove_root_latest_artifacts(ctx: ProjectContext, *, kinds: tuple[str, ...] = ("source", "review", "vf")) -> list[str]:
    """Remove obsolete root-level *-latest artifacts from the upload surface.

    Dated logs are preserved. This intentionally affects only files directly
    under the project import root so historical run artifacts remain available.
    """
    root = import_root(ctx)
    removed: list[str] = []
    suffixes = {
        "source": (".zip",),
        "review": (".zip",),
        "vf": (".md", ".json"),
    }
    for kind in kinds:
        for suffix in suffixes.get(kind, ()):  # defensive: unknown kinds remove nothing
            path = root / f"{ctx.project_id}-{kind}-latest{suffix}"
            if path.exists() and path.is_file():
                path.unlink()
                removed.append(str(path))
    return removed


def publish_source_upload_alias(ctx: ProjectContext, source_path: Path, *, head: str | None = None, now: datetime | None = None) -> UploadAliasResult:
    return _publish_file_alias(ctx, kind="source", src=source_path, suffix=".zip", head=head, now=now)


def publish_review_upload_alias(ctx: ProjectContext, review_path: Path, *, head: str | None = None, now: datetime | None = None) -> UploadAliasResult:
    return _publish_file_alias(ctx, kind="review", src=review_path, suffix=".zip", head=head, now=now)


def publish_verify_upload_alias(
    ctx: ProjectContext,
    markdown_path: Path,
    *,
    json_path: Path | None = None,
    head: str | None = None,
    now: datetime | None = None,
) -> UploadAliasResult:
    """Publish a root upload alias for verify markdown and dated md/json aliases.

    The root intentionally receives only the markdown alias, because that is the
    human/LLM upload artifact. Commit-named JSON aliases are stored only in the
    dated verify log folder.
    """
    result = _publish_file_alias(ctx, kind="vf", src=markdown_path, suffix=".md", head=head, now=now, log_kind="verify")
    if json_path and json_path.exists():
        stamp = now or datetime.now()
        full_head = _head(ctx, head)
        head7 = full_head[:7]
        dated_json = _dated_dir(ctx, "verify", stamp) / f"{ctx.project_id}-vf-{head7}.json"
        _copy_replace(json_path, dated_json)
        result.dated_json_alias = str(dated_json)
    return result


def _publish_file_alias(
    ctx: ProjectContext,
    *,
    kind: str,
    src: Path,
    suffix: str,
    head: str | None,
    now: datetime | None,
    log_kind: str | None = None,
) -> UploadAliasResult:
    src = Path(src)
    full_head = _head(ctx, head)
    head7 = full_head[:7]
    stamp = now or datetime.now()
    root = mkdirp(import_root(ctx))
    dated = _dated_dir(ctx, log_kind or kind, stamp)
    root_alias = root / f"{ctx.project_id}-{kind}-{head7}{suffix}"
    dated_alias = dated / f"{ctx.project_id}-{kind}-{head7}{suffix}"
    removed = _prune_root_aliases(root, ctx.project_id, kind=kind, suffix=suffix, keep_name=root_alias.name)
    _copy_replace(src, root_alias)
    _copy_replace(src, dated_alias)
    return UploadAliasResult(
        kind=kind,
        head=full_head,
        root_alias=str(root_alias),
        dated_alias=str(dated_alias),
        removed_root_aliases=removed,
    )


def _dated_dir(ctx: ProjectContext, kind: str, stamp: datetime) -> Path:
    return mkdirp(import_root(ctx) / "logs" / kind / stamp.strftime("%y%m%d"))


def _head(ctx: ProjectContext, explicit: str | None) -> str:
    if explicit:
        return explicit
    try:
        return git_head(ctx.repo_path)
    except Exception:
        return "unknown"


def _copy_replace(src: Path, dst: Path) -> None:
    if not src.exists():
        raise FileNotFoundError(f"upload alias source missing: {src}")
    mkdirp(dst.parent)
    try:
        if src.resolve() == dst.resolve():
            return
    except OSError:
        pass
    tmp = dst.with_name(f".{dst.name}.tmp")
    if tmp.exists():
        tmp.unlink()
    shutil.copy2(src, tmp)
    if dst.exists():
        dst.unlink()
    tmp.replace(dst)


def _prune_root_aliases(root: Path, project: str, *, kind: str, suffix: str, keep_name: str) -> list[str]:
    pattern = re.compile(rf"^{re.escape(project)}-{re.escape(kind)}-[0-9a-f]{{7,40}}{re.escape(suffix)}$")
    removed: list[str] = []
    if not root.exists():
        return removed
    for path in root.iterdir():
        if not path.is_file() or path.name == keep_name:
            continue
        if pattern.match(path.name):
            path.unlink()
            removed.append(str(path))
    return removed
