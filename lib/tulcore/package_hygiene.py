"""Package inbox hygiene planning, ingest, and quarantine moves."""
from __future__ import annotations

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
)


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
    inbox_root: Path
    quarantine_root: Path
    matching_count: int
    incompatible_count: int
    invalid_count: int
    duplicate_groups: dict[str, list[str]]
    actions: list[HygieneAction]
    report_only_invalid: list[dict[str, Any]]

    @property
    def move_count(self) -> int:
        return sum(1 for action in self.actions if action.moved)

    @property
    def ingest_actions(self) -> list[HygieneAction]:
        return [action for action in self.actions if action.kind == "ingest"]

    @property
    def cleanup_actions(self) -> list[HygieneAction]:
        return [action for action in self.actions if action.kind != "ingest"]

    def as_dict(self) -> dict[str, Any]:
        return {
            "project": self.project,
            "repo": self.repo,
            "branch": self.branch,
            "mode": self.mode,
            "inbox_root": str(self.inbox_root),
            "quarantine_root": str(self.quarantine_root),
            "matching_count": self.matching_count,
            "incompatible_count": self.incompatible_count,
            "invalid_count": self.invalid_count,
            "duplicate_groups": self.duplicate_groups,
            "actions": [action.as_dict() for action in self.actions],
            "report_only_invalid": self.report_only_invalid,
            "move_count": self.move_count,
        }


def package_project_root(global_config: dict, *, project: str) -> Path:
    paths = platform_paths(global_config)
    work_root = paths.get("work_root")
    archive_root = paths.get("archive_root")
    if work_root:
        return Path(work_root).parent
    if archive_root:
        return Path(archive_root).parent
    return Path.home() / ".cache" / "tul" / project


def package_inbox_root(global_config: dict, *, project: str) -> Path:
    return package_project_root(global_config, project=project) / "inbox"


def package_quarantine_root(global_config: dict, *, project: str) -> Path:
    return package_project_root(global_config, project=project) / "package-quarantine" / project


def _safe_size(path: Path) -> int | None:
    try:
        return path.stat().st_size
    except OSError:
        return None


def _is_inside(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except Exception:
        return False


def _unique_destination(root: Path, source: Path, *, kind: str) -> Path:
    stamp = datetime.now().strftime("%Y%m%d")
    dest_dir = root / stamp / kind
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


def _inbox_destination(inbox_root: Path, source: Path) -> Path:
    dest = inbox_root / source.name
    if not dest.exists():
        return dest
    stem = source.stem
    suffix = source.suffix
    counter = 1
    while True:
        candidate = inbox_root / f"{stem}-{counter}{suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def _duplicate_groups(candidates: list[PackageCandidate]) -> dict[str, list[PackageCandidate]]:
    groups: dict[str, list[PackageCandidate]] = {}
    for item in candidates:
        groups.setdefault(item.name, []).append(item)
    return {name: sorted(items, key=lambda item: item.mtime, reverse=True) for name, items in groups.items() if len(items) > 1}


def _action_for_inbox_invalid(item: InvalidPackageCandidate, quarantine_root: Path) -> HygieneAction:
    return HygieneAction(
        kind="invalid",
        source=item.source,
        destination=_unique_destination(quarantine_root, item.source, kind="invalid"),
        reason=f"invalid archive in project inbox: {item.reason}",
        size=_safe_size(item.source),
        mtime=item.mtime,
    )


def _action_for_duplicate(item: PackageCandidate, quarantine_root: Path, *, kept_name: str) -> HygieneAction:
    return HygieneAction(
        kind="duplicate",
        source=item.source,
        destination=_unique_destination(quarantine_root, item.source, kind="duplicate"),
        reason=f"older duplicate matching package in project inbox for name={kept_name!r}",
        size=_safe_size(item.source),
        mtime=item.mtime,
    )


def _action_for_ingest(item: PackageCandidate, inbox_root: Path) -> HygieneAction:
    return HygieneAction(
        kind="ingest",
        source=item.source,
        destination=_inbox_destination(inbox_root, item.source),
        reason="valid matching tul package outside project inbox",
        size=_safe_size(item.source),
        mtime=item.mtime,
    )


def plan_package_hygiene(
    ctx: ProjectContext,
    *,
    keep_duplicates: int = 1,
    include_invalid: bool = True,
    include_duplicates: bool = True,
    include_ingest: bool = True,
) -> PackageHygieneResult:
    branch = current_branch(ctx.repo_path)
    expected_branch = ctx.expected_branch or branch
    inventory = discover_package_inventory(
        ctx.global_config,
        project=ctx.project_id,
        repo=ctx.expected_repo,
        branch=expected_branch,
    )
    inbox_root = package_inbox_root(ctx.global_config, project=ctx.project_id)
    quarantine_root = package_quarantine_root(ctx.global_config, project=ctx.project_id)
    actions: list[HygieneAction] = []

    inbox_matching = [item for item in inventory.matching if _is_inside(item.source, inbox_root)]
    external_matching = [item for item in inventory.matching if not _is_inside(item.source, inbox_root)]
    inbox_invalid = [item for item in inventory.invalid if _is_inside(item.source, inbox_root)]
    report_only_invalid = [invalid_candidate_record(item) for item in inventory.invalid if not _is_inside(item.source, inbox_root)]

    if include_ingest:
        actions.extend(_action_for_ingest(item, inbox_root) for item in external_matching)

    if include_invalid:
        actions.extend(_action_for_inbox_invalid(item, quarantine_root) for item in inbox_invalid)

    groups = _duplicate_groups(inbox_matching)
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
        inbox_root=inbox_root,
        quarantine_root=quarantine_root,
        matching_count=len(inventory.matching),
        incompatible_count=len(inventory.incompatible),
        invalid_count=len(inventory.invalid),
        duplicate_groups={name: [str(item.source) for item in items] for name, items in groups.items()},
        actions=sorted(actions, key=lambda action: action.mtime, reverse=True),
        report_only_invalid=sorted(report_only_invalid, key=lambda item: float(item.get("mtime_epoch") or 0), reverse=True),
    )


def run_package_hygiene(
    ctx: ProjectContext,
    *,
    ingest: bool = False,
    quarantine: bool = False,
    keep_duplicates: int = 1,
    include_invalid: bool = True,
    include_duplicates: bool = True,
    include_ingest: bool = True,
) -> PackageHygieneResult:
    result = plan_package_hygiene(
        ctx,
        keep_duplicates=keep_duplicates,
        include_invalid=include_invalid,
        include_duplicates=include_duplicates,
        include_ingest=include_ingest,
    )
    if ingest and quarantine:
        result.mode = "ingest+quarantine"
    elif ingest:
        result.mode = "ingest"
    elif quarantine:
        result.mode = "quarantine"
    else:
        result.mode = "dry-run"
    if not ingest and not quarantine:
        return result
    for action in result.actions:
        if action.kind == "ingest" and not ingest:
            continue
        if action.kind != "ingest" and not quarantine:
            continue
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


def _format_action(action: HygieneAction) -> list[str]:
    moved = " moved" if action.moved else ""
    if action.error:
        moved = f" error={action.error}"
    return [
        f"- [{action.kind}]{moved} {action.source}",
        f"  destination: {action.destination}",
        f"  reason: {action.reason}",
    ]


def format_package_hygiene(result: PackageHygieneResult, *, limit: int = 50) -> str:
    ingest_actions = result.ingest_actions
    cleanup_actions = result.cleanup_actions
    lines = [
        "# tul package hygiene",
        f"Project: {result.project}",
        f"Repo: {result.repo or '(not configured)'}",
        f"Branch: {result.branch or '(unknown)'}",
        f"Mode: {result.mode}",
        f"Project inbox: {result.inbox_root}",
        f"Quarantine root: {result.quarantine_root}",
        "",
        "Inventory:",
        f"- matching: {result.matching_count}",
        f"- duplicate groups in project inbox: {len(result.duplicate_groups)}",
        f"- incompatible: {result.incompatible_count}",
        f"- invalid: {result.invalid_count}",
        f"- ingest candidates: {len(ingest_actions)}",
        f"- inbox cleanup candidates: {len(cleanup_actions)}",
        f"- report-only external invalid: {len(result.report_only_invalid)}",
    ]
    if result.move_count:
        lines.append(f"- moved: {result.move_count}")
    if result.duplicate_groups:
        lines.extend(["", "Duplicate matching package groups in project inbox:"])
        for name, paths in sorted(result.duplicate_groups.items()):
            lines.append(f"- {name}: {len(paths)} file(s)")
            for path in paths[:3]:
                lines.append(f"  - {path}")
            if len(paths) > 3:
                lines.append(f"  - ... {len(paths) - 3} more")
    lines.append("")

    shown = 0
    if ingest_actions:
        if result.mode in {"ingest", "ingest+quarantine"}:
            lines.append(f"Ingest actions for {len(ingest_actions)} valid matching package archive(s):")
        else:
            lines.append(f"Would ingest {len(ingest_actions)} valid matching package archive(s):")
        for action in ingest_actions[: max(limit, 0)]:
            lines.extend(_format_action(action))
            shown += 1
        lines.append("")

    if cleanup_actions:
        if result.mode in {"quarantine", "ingest+quarantine"}:
            lines.append(f"Quarantine actions for {len(cleanup_actions)} project inbox archive(s):")
        else:
            lines.append(f"Would quarantine {len(cleanup_actions)} project inbox archive(s):")
        remaining_limit = max(limit - shown, 0)
        for action in cleanup_actions[:remaining_limit]:
            lines.extend(_format_action(action))
            shown += 1
        lines.append("")

    hidden = len(result.actions) - shown
    if hidden > 0:
        lines.append(f"... {hidden} more action(s) not shown")
        lines.append("")

    if result.report_only_invalid:
        lines.append("Report-only external invalid archive(s), not selected for quarantine:")
        for item in result.report_only_invalid[: max(limit, 0)]:
            lines.append(f"- {item.get('path')}")
            lines.append(f"  reason: {item.get('reason')}")
        if len(result.report_only_invalid) > limit:
            lines.append(f"- ... {len(result.report_only_invalid) - limit} more")
        lines.append("")

    if not result.actions:
        lines.append("No package hygiene actions selected.")
    elif result.mode == "dry-run":
        lines.append("No files were moved. Review the list, then re-run with --ingest and/or --quarantine only if it is correct.")
    else:
        lines.append("Package hygiene complete. Files were moved, not deleted.")
    return "\n".join(lines).rstrip()
