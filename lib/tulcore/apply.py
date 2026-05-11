"""Safe copy application for manifest packages.

The apply layer must be conservative because it is the point where an
LLM-generated package can overwrite repository files. It now builds a concrete
apply plan before copying, rejects implicit directory copies, and verifies that
every planned destination is covered by manifest commit.files.
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

from .errors import SafetyError
from .manifest import Manifest
from .paths import mkdirp, repo_relative, safe_join


def apply_copy(
    manifest: Manifest,
    *,
    extracted_dir: Path,
    repo_path: Path,
    backup_dir: Path,
    log_path: Path,
    plan_path: Path | None = None,
    allowed_files: list[str] | None = None,
) -> list[str]:
    """Apply ``apply.mode: copy`` after building and validating an apply plan.

    Safety rules:
    - each source/destination path must stay within its expected root;
    - copying a directory requires ``allow_directory: true`` on that item;
    - every planned destination must be listed in ``commit.files``;
    - duplicate destinations are rejected before any copy occurs.
    """
    allowed = allowed_files if allowed_files is not None else manifest.commit_files
    planned = build_apply_plan(
        manifest,
        extracted_dir=extracted_dir,
        repo_path=repo_path,
        allowed_files=allowed,
    )
    if plan_path is None:
        plan_path = log_path.with_name("apply-plan.json")
    write_apply_plan(plan_path, planned)

    changed: list[str] = []
    mkdirp(backup_dir)
    logs: list[str] = []
    for item in planned:
        src = Path(str(item["source_abs"]))
        dst = Path(str(item["destination_abs"]))
        _copy_one(src, dst, repo_path=repo_path, backup_dir=backup_dir, logs=logs)
        changed.append(str(item["destination"]))
    log_path.write_text("\n".join(logs) + ("\n" if logs else ""), encoding="utf-8", newline="\n")
    return sorted(set(changed))


def build_apply_plan(
    manifest: Manifest,
    *,
    extracted_dir: Path,
    repo_path: Path,
    allowed_files: list[str],
) -> list[dict[str, Any]]:
    operations = manifest.apply.get("files") or []
    allowed = {str(item) for item in allowed_files}
    planned: list[dict[str, Any]] = []
    seen: set[str] = set()

    for index, item in enumerate(operations):
        if not isinstance(item, dict):
            raise SafetyError(f"apply.files[{index}] must be a mapping")
        src_rel = str(item["from"])
        dst_rel = str(item["to"])
        src = safe_join(extracted_dir, src_rel)
        dst = safe_join(repo_path, dst_rel)
        if not src.exists():
            raise SafetyError(f"manifest source does not exist: {src_rel}")

        if src.is_dir():
            if item.get("allow_directory") is not True:
                raise SafetyError(
                    "directory copy requires allow_directory: true "
                    f"for apply.files[{index}]: {src_rel} -> {dst_rel}"
                )
            children = sorted(p for p in src.rglob("*") if p.is_file())
            if not children:
                raise SafetyError(f"directory copy source has no files: {src_rel}")
            for child in children:
                child_rel = child.relative_to(src).as_posix()
                target = safe_join(dst, child_rel)
                _append_plan_item(
                    planned,
                    seen,
                    source=child,
                    destination=target,
                    repo_path=repo_path,
                    extracted_dir=extracted_dir,
                    operation_index=index,
                    directory=True,
                    source_root=src_rel,
                    destination_root=dst_rel,
                    allowed=allowed,
                )
        else:
            _append_plan_item(
                planned,
                seen,
                source=src,
                destination=dst,
                repo_path=repo_path,
                extracted_dir=extracted_dir,
                operation_index=index,
                directory=False,
                source_root=None,
                destination_root=None,
                allowed=allowed,
            )
    return planned


def _append_plan_item(
    planned: list[dict[str, Any]],
    seen: set[str],
    *,
    source: Path,
    destination: Path,
    repo_path: Path,
    extracted_dir: Path,
    operation_index: int,
    directory: bool,
    source_root: str | None,
    destination_root: str | None,
    allowed: set[str],
) -> None:
    rel_destination = repo_relative(repo_path, destination)
    if rel_destination in seen:
        raise SafetyError(f"duplicate apply destination: {rel_destination}")
    seen.add(rel_destination)
    if rel_destination not in allowed:
        raise SafetyError(
            "apply destination outside manifest commit.files: "
            f"{rel_destination}\nAdd it to commit.files or narrow apply.files."
        )
    planned.append(
        {
            "operation_index": operation_index,
            "source": source.relative_to(extracted_dir.resolve()).as_posix(),
            "destination": rel_destination,
            "source_abs": str(source),
            "destination_abs": str(destination),
            "directory_copy": directory,
            "source_root": source_root,
            "destination_root": destination_root,
            "will_backup": destination.exists(),
            "size_bytes": source.stat().st_size,
        }
    )


def write_apply_plan(path: Path, planned: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    public_plan = [
        {key: value for key, value in item.items() if key not in {"source_abs", "destination_abs"}}
        for item in planned
    ]
    path.write_text(
        json.dumps({"version": 1, "operation_count": len(public_plan), "operations": public_plan}, indent=2, ensure_ascii=False)
        + "\n",
        encoding="utf-8",
        newline="\n",
    )


def _copy_one(src: Path, dst: Path, *, repo_path: Path, backup_dir: Path, logs: list[str]) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        rel = dst.relative_to(repo_path).as_posix()
        backup = backup_dir / rel
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(dst, backup)
        logs.append(f"backup {rel} -> {backup}")
    shutil.copy2(src, dst)
    logs.append(f"copy {src} -> {dst}")
