"""Package authoring helpers for tul."""
from __future__ import annotations

import json
import tarfile
import tempfile
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .apply import build_apply_plan
from .config import dump_yaml
from .errors import TulError
from .manifest import Manifest, load_manifest, validate_manifest
from .package import manifest_data_from_archive, safe_extract, sha256_file
from .paths import mkdirp

FORBIDDEN_ARCHIVE_PARTS = {"__pycache__", ".git"}
FORBIDDEN_SUFFIXES = {".pyc", ".pyo"}


@dataclass
class PackageCheckResult:
    path: Path
    ok: bool
    checks: list[dict[str, Any]]
    manifest: dict[str, Any]
    sha256: str | None = None
    apply_plan_count: int | None = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "path": str(self.path),
            "ok": self.ok,
            "sha256": self.sha256,
            "manifest": self.manifest,
            "apply_plan_count": self.apply_plan_count,
            "checks": self.checks,
        }


def _add(checks: list[dict[str, Any]], ok: bool, name: str, detail: str = "") -> None:
    checks.append({"ok": bool(ok), "name": name, "detail": detail})


def _archive_names(path: Path) -> list[str]:
    if zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as zf:
            return zf.namelist()
    if tarfile.is_tarfile(path):
        with tarfile.open(path) as tf:
            return [member.name for member in tf.getmembers()]
    raise TulError(f"unsupported package archive: {path}")


def _has_forbidden_member(names: list[str]) -> list[str]:
    bad: list[str] = []
    for name in names:
        parts = [part for part in name.replace("\\", "/").split("/") if part]
        if any(part in FORBIDDEN_ARCHIVE_PARTS for part in parts) or any(name.endswith(suffix) for suffix in FORBIDDEN_SUFFIXES):
            bad.append(name)
    return bad


def check_package_archive(path: Path, *, ctx: Any | None = None) -> PackageCheckResult:
    path = path.expanduser().resolve()
    checks: list[dict[str, Any]] = []
    manifest_data: dict[str, Any] = {}
    digest: str | None = None
    apply_plan_count: int | None = None

    _add(checks, path.exists(), "archive exists", str(path))
    if not path.exists():
        return PackageCheckResult(path=path, ok=False, checks=checks, manifest={})

    try:
        names = _archive_names(path)
        _add(checks, True, "archive readable", f"{len(names)} entries")
    except Exception as exc:
        _add(checks, False, "archive readable", str(exc))
        return PackageCheckResult(path=path, ok=False, checks=checks, manifest={})

    _add(checks, "tul-package.yml" in names, "root tul-package.yml", "must be at archive root")
    _add(checks, "README.md" in names, "root README.md", "recommended package instructions")
    _add(checks, any(name.startswith("files/") for name in names), "files/ payload", "repo files must live under files/")

    bad = _has_forbidden_member(names)
    _add(checks, not bad, "no generated/cache files", ", ".join(bad[:5]) if bad else "ok")

    try:
        manifest_data = manifest_data_from_archive(path)
        digest = sha256_file(path)
        _add(checks, True, "manifest parse", str(manifest_data.get("name") or path.stem))
    except Exception as exc:
        _add(checks, False, "manifest parse", str(exc))

    if manifest_data:
        manifest = Manifest(path=Path("tul-package.yml"), data=manifest_data)
        try:
            # Basic validation without target context is still useful.
            if ctx is None:
                project = str((manifest.target or {}).get("project") or "")
                repo = str((manifest.target or {}).get("repo") or "")
                branch = str((manifest.target or {}).get("branch") or "")
            else:
                project = ctx.project_id
                repo = ctx.expected_repo
                branch = ctx.expected_branch
            validate_manifest(manifest, project=project, repo=repo, branch=branch)
            _add(checks, True, "manifest validation", "ok")
        except Exception as exc:
            _add(checks, False, "manifest validation", str(exc))

        if ctx is not None:
            try:
                with tempfile.TemporaryDirectory(prefix="tul-package-check-") as tmp:
                    extracted = Path(tmp) / "extracted"
                    safe_extract(path, extracted)
                    extracted_manifest = load_manifest(extracted / "tul-package.yml")
                    plan = build_apply_plan(
                        extracted_manifest,
                        extracted_dir=extracted,
                        repo_path=ctx.repo_path,
                        allowed_files=extracted_manifest.commit_files,
                    )
                    apply_plan_count = len(plan)
                    _add(checks, True, "apply plan", f"{len(plan)} operation(s)")
            except Exception as exc:
                _add(checks, False, "apply plan", str(exc))

    ok = all(item.get("ok") for item in checks)
    return PackageCheckResult(path=path, ok=ok, checks=checks, manifest=manifest_data, sha256=digest, apply_plan_count=apply_plan_count)


def format_package_check(result: PackageCheckResult) -> str:
    lines = ["# tul package check", "", f"Package: {result.path}", f"Result: {'pass' if result.ok else 'fail'}"]
    if result.sha256:
        lines.append(f"Sha256: {result.sha256}")
    manifest = result.manifest or {}
    target = manifest.get("target") or {}
    if manifest:
        lines.append(f"Name: {manifest.get('name') or result.path.stem}")
        lines.append(f"Target: {target.get('project')} {target.get('repo')} {target.get('branch')}")
    if result.apply_plan_count is not None:
        lines.append(f"Apply plan operations: {result.apply_plan_count}")
    lines.append("")
    lines.append("## Checks")
    for item in result.checks:
        mark = "PASS" if item.get("ok") else "FAIL"
        lines.append(f"- [{mark}] {item.get('name')}")
        detail = str(item.get("detail") or "").strip()
        if detail:
            lines.append(f"  {detail}")
    return "\n".join(lines)


def scaffold_package_dir(
    name: str,
    *,
    out_dir: Path,
    project: str,
    repo: str,
    branch: str,
    message: str,
    force: bool = False,
) -> Path:
    package_dir = (out_dir.expanduser().resolve() / name) if out_dir.name != name else out_dir.expanduser().resolve()
    if package_dir.exists() and any(package_dir.iterdir()) and not force:
        raise TulError(f"package directory already exists and is not empty: {package_dir}")
    mkdirp(package_dir)
    mkdirp(package_dir / "files")
    manifest = {
        "version": 1,
        "name": name.replace("_", "-"),
        "target": {"project": project, "repo": repo, "branch": branch},
        "apply": {"mode": "copy", "files": []},
        "commit": {"files": [], "message": message},
    }
    (package_dir / "tul-package.yml").write_text(dump_yaml(manifest) + "\n", encoding="utf-8")
    (package_dir / "README.md").write_text(
        f"# {name}\n\n"
        "This is a tul package scaffold.\n\n"
        "Add repo files under `files/`, then edit `tul-package.yml` so `apply.files` and `commit.files` list the exact repo-relative files to update.\n\n"
        "Validate before use:\n\n"
        "```bash\n"
        f"tul package zip {package_dir} --out {package_dir.with_suffix('.zip')}\n"
        f"tul package check {package_dir.with_suffix('.zip')} --target {project}\n"
        "```\n",
        encoding="utf-8",
    )
    (package_dir / "files" / ".gitkeep").write_text("", encoding="utf-8")
    return package_dir


def should_skip_zip_member(path: Path) -> bool:
    parts = set(path.parts)
    if parts & FORBIDDEN_ARCHIVE_PARTS:
        return True
    if path.suffix in FORBIDDEN_SUFFIXES:
        return True
    if path.name in {".DS_Store"}:
        return True
    return False


def zip_package_dir(package_dir: Path, *, out_path: Path | None = None, force: bool = False) -> Path:
    package_dir = package_dir.expanduser().resolve()
    if not package_dir.is_dir():
        raise TulError(f"package directory does not exist: {package_dir}")
    if not (package_dir / "tul-package.yml").exists():
        raise TulError(f"missing root tul-package.yml in package dir: {package_dir}")
    if not (package_dir / "README.md").exists():
        raise TulError(f"missing root README.md in package dir: {package_dir}")
    if not (package_dir / "files").is_dir():
        raise TulError(f"missing files/ payload directory in package dir: {package_dir}")
    out = out_path.expanduser().resolve() if out_path else package_dir.with_suffix(".zip")
    if out.exists() and not force:
        raise TulError(f"output archive already exists: {out}; use --force to replace")
    mkdirp(out.parent)
    tmp = out.with_suffix(out.suffix + ".tmp")
    if tmp.exists():
        tmp.unlink()
    with zipfile.ZipFile(tmp, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for item in sorted(package_dir.rglob("*")):
            if item.is_dir() or should_skip_zip_member(item):
                continue
            arcname = item.relative_to(package_dir).as_posix()
            zf.write(item, arcname)
    tmp.replace(out)
    # Validate root layout after writing; this catches accidental nested dirs
    # without requiring scaffold manifests to be fully populated yet.
    names = _archive_names(out)
    if "tul-package.yml" not in names or "README.md" not in names or not any(name.startswith("files/") for name in names):
        raise TulError(f"created archive has invalid root layout: {out}")
    return out
