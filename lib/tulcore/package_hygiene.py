"""Package inbox hygiene planning and quarantine moves."""
from __future__ import annotations

import json
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from .config import ProjectContext, platform_paths
from .gitops import current_branch
from .package import (
    InvalidPackageCandidate,
    PackageCandidate,
    discover_package_inventory,
    invalid_candidate_record,
    candidate_record,
)
from .paths import mkdirp


@dataclass
class HygieneAction:
    kind: str
    source: Path
    destination: Path
    reason: str
    size: int | None
    mtime: float
    moved: bool = False
    error: str | None = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "source": str(self.source),
            "destination": str(self.destination),
            "reason": self.reason,
            "size": self.size,
            "mtime": datetime.fromtimestamp(self.mtime).astimezone().isoformat(timespec="seconds"),
            "mtime_epoch": self.mtime,
            "moved": self.moved,
            "error": self.error,
        }


@dataclass
class PackageHygieneResult:
    project: str
    repo: str | None
    branch: str | None
    mode: str
    quarantine_root: Path
    matching_count: int
    incompatible_count: int
    invalid_count: int
    duplicate_groups: dict[str, list[str]]
    actions: list[HygieneAction]

    @property
    def move_count(self) -> int:
        return sum(1 for action in self.actions if action.moved)

    def as_dict(self) -> dict[str, Any]:
        return {
            "project": self.project,
            "repo": self.repo,
            "branch": self.branch,
            "mode": self.mode,
            "quarantine_root": str(self.quarantine_root),
            "matching_count": self.matching_count,
            "incompatible_count": self.incompatible_count,
            "invalid_count": self.invalid_count,
            "duplicate_groups": self.duplicate_groups,
            "actions": [action.as_dict() for action in self.actions],
            "move_count": self.move_count,
        }


def package_quarantine_root(global_config: dict, *, project: str) -> Path:
    paths = platform_paths(global_config)
    work_root = paths.get("work_root")
    archive_root = paths.get("archive_root")
    if work_root:
        base = Path(work_root).parent
    elif archive_root:
        base = Path(archive_root).parent
    else:
        base = Path.home() / ".cache" / "tul"
    return base / "package-quarantine" / project


def _safe_size(path: Path) -> int | None:
    try:
        return path.stat().st_size
    except OSError:
        return None


def _unique_destination(root: Path, source: Path, *, kind: str) -> Path:
    stamp = datetime.now().strftime("%Y%m%d")
    dest_dir = root / stamp / kind
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / source.name
    if not dest.exists():
        return dest
    stem = source.stem
    suffix = source.suffix
    counter = 1
    while True:
        candidate = dest_dir / f"{stem}-{counter}{suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def _duplicate_groups(candidates: list[PackageCandidate]) -> dict[str, list[PackageCandidate]]:
    groups: dict[str, list[PackageCandidate]] = {}
    for item in candidates:
        groups.setdefault(item.name, []).append(item)
    return {name: sorted(items, key=lambda item: item.mtime, reverse=True) for name, items in groups.items() if len(items) > 1}


def _action_for_invalid(item: InvalidPackageCandidate, quarantine_root: Path) -> HygieneAction:
    return HygieneAction(
        kind="invalid",
        source=item.source,
        destination=_unique_destination(quarantine_root, item.source, kind="invalid"),
        reason=item.reason,
        size=_safe_size(item.source),
        mtime=item.mtime,
    )


def _action_for_duplicate(item: PackageCandidate, quarantine_root: Path, *, kept_name: str) -> HygieneAction:
    return HygieneAction(
        kind="duplicate",
        source=item.source,
        destination=_unique_destination(quarantine_root, item.source, kind="duplicate"),
        reason=f"older duplicate matching package for name={kept_name!r}",
        size=_safe_size(item.source),
        mtime=item.mtime,
    )


def plan_package_hygiene(
    ctx: ProjectContext,
    *,
    keep_duplicates: int = 1,
    include_invalid: bool = True,
    include_duplicates: bool = True,
) -> PackageHygieneResult:
    branch = current_branch(ctx.repo_path)
    expected_branch = ctx.expected_branch or branch
    inventory = discover_package_inventory(
        ctx.global_config,
        project=ctx.project_id,
        repo=ctx.expected_repo,
        branch=expected_branch,
    )
    quarantine_root = package_quarantine_root(ctx.global_config, project=ctx.project_id)
    actions: list[HygieneAction] = []

    if include_invalid:
        actions.extend(_action_for_invalid(item, quarantine_root) for item in inventory.invalid)

    groups = _duplicate_groups(inventory.matching)
    if include_duplicates:
        keep = max(int(keep_duplicates), 1)
        for name, items in groups.items():
            for item in items[keep:]:
                actions.append(_action_for_duplicate(item, quarantine_root, kept_name=name))

    return PackageHygieneResult(
        project=ctx.project_id,
        repo=ctx.expected_repo,
        branch=expected_branch,
        mode="dry-run",
        quarantine_root=quarantine_root,
        matching_count=len(inventory.matching),
        incompatible_count=len(inventory.incompatible),
        invalid_count=len(inventory.invalid),
        duplicate_groups={name: [str(item.source) for item in items] for name, items in groups.items()},
        actions=sorted(actions, key=lambda action: action.mtime, reverse=True),
    )


def run_package_hygiene(
    ctx: ProjectContext,
    *,
    quarantine: bool = False,
    keep_duplicates: int = 1,
    include_invalid: bool = True,
    include_duplicates: bool = True,
) -> PackageHygieneResult:
    result = plan_package_hygiene(
        ctx,
        keep_duplicates=keep_duplicates,
        include_invalid=include_invalid,
        include_duplicates=include_duplicates,
    )
    result.mode = "quarantine" if quarantine else "dry-run"
    if not quarantine:
        return result
    for action in result.actions:
        try:
            if not action.source.exists():
                action.error = "source missing"
                continue
            action.destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(action.source), str(action.destination))
            action.moved = True
        except Exception as exc:  # pragma: no cover - defensive; surfaced to CLI.
            action.error = str(exc)
    return result


def format_package_hygiene(result: PackageHygieneResult, *, limit: int = 50) -> str:
    lines = [
        "# tul package hygiene",
        f"Project: {result.project}",
        f"Repo: {result.repo or '(not configured)'}",
        f"Branch: {result.branch or '(unknown)'}",
        f"Mode: {result.mode}",
        f"Quarantine root: {result.quarantine_root}",
        "",
        "Inventory:",
        f"- matching: {result.matching_count}",
        f"- duplicate groups: {len(result.duplicate_groups)}",
        f"- incompatible: {result.incompatible_count}",
        f"- invalid: {result.invalid_count}",
        f"- selected for hygiene: {len(result.actions)}",
    ]
    if result.move_count:
        lines.append(f"- moved: {result.move_count}")
    if result.duplicate_groups:
        lines.extend(["", "Duplicate matching package groups:"])
        for name, paths in sorted(result.duplicate_groups.items()):
            lines.append(f"- {name}: {len(paths)} file(s)")
            for path in paths[:3]:
                lines.append(f"  - {path}")
            if len(paths) > 3:
                lines.append(f"  - ... {len(paths) - 3} more")
    lines.append("")
    if not result.actions:
        lines.append("No package hygiene actions selected.")
        return "\n".join(lines)
    if result.mode == "dry-run":
        lines.append(f"Would quarantine {len(result.actions)} package archive(s):")
    else:
        lines.append(f"Quarantine actions for {len(result.actions)} package archive(s):")
    for action in result.actions[: max(limit, 0)]:
        moved = " moved" if action.moved else ""
        if action.error:
            moved = f" error={action.error}"
        lines.extend([
            f"- [{action.kind}]{moved} {action.source}",
            f"  destination: {action.destination}",
            f"  reason: {action.reason}",
        ])
    if len(result.actions) > limit:
        lines.append(f"... {len(result.actions) - limit} more action(s) not shown")
    if result.mode == "dry-run":
        lines.extend([
            "",
            "No files were moved. Review the list, then re-run with --quarantine only if it is correct.",
        ])
    else:
        lines.extend([
            "",
            "Quarantine complete. Quarantined files were moved, not deleted.",
        ])
    return "\n".join(lines)
