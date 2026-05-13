"""Package discovery, import, and safe extraction."""
from __future__ import annotations

import hashlib
import shutil
import tarfile
import zipfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from .config import platform_paths
from .errors import PackageError, SafetyError
from .manifest import Manifest, load_manifest
from .paths import ensure_inside, mkdirp, safe_join


@dataclass
class PackageCandidate:
    source: Path
    manifest_data: dict
    mtime: float
    reason: str = ""

    @property
    def name(self) -> str:
        return str(self.manifest_data.get("name") or self.source.stem)


@dataclass
class InvalidPackageCandidate:
    source: Path
    mtime: float
    reason: str


@dataclass
class PackageDiscovery:
    matching: list[PackageCandidate]
    incompatible: list[PackageCandidate]
    invalid: list[InvalidPackageCandidate]


@dataclass
class ImportedPackage:
    source: Path
    work_dir: Path
    extracted_dir: Path
    manifest: Manifest
    sha256: str


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _archive_names(path: Path) -> list[str] | None:
    try:
        if zipfile.is_zipfile(path):
            with zipfile.ZipFile(path) as zf:
                return zf.namelist()
        if tarfile.is_tarfile(path):
            with tarfile.open(path) as tf:
                return [member.name for member in tf.getmembers()]
    except Exception:
        return None
    return None


def _root_manifest_diagnostic(path: Path) -> str:
    names = _archive_names(path)
    if names is None:
        return "unsupported or unreadable archive; expected .zip or .tar.gz"
    normalized = [name.replace("\\", "/").lstrip("./") for name in names]
    nested = [name for name in normalized if name.endswith("/tul-package.yml")]
    if nested:
        examples = ", ".join(nested[:3])
        return f"missing root tul-package.yml; found nested manifest(s): {examples}"
    return "missing or unreadable root tul-package.yml"


def _manifest_from_archive(path: Path) -> dict | None:
    try:
        if zipfile.is_zipfile(path):
            with zipfile.ZipFile(path) as zf:
                try:
                    raw = zf.read("tul-package.yml").decode("utf-8")
                except KeyError:
                    return None
        elif tarfile.is_tarfile(path):
            with tarfile.open(path) as tf:
                try:
                    member = tf.getmember("tul-package.yml")
                except KeyError:
                    return None
                extracted = tf.extractfile(member)
                if extracted is None:
                    return None
                raw = extracted.read().decode("utf-8")
        else:
            return None
    except Exception:
        return None
    from .config import load_yaml_text

    try:
        return load_yaml_text(raw)
    except Exception:
        return None


def manifest_data_from_archive(path: Path) -> dict:
    """Read tul-package.yml from an archive without extracting it."""
    path = Path(path).expanduser().resolve()
    if not path.exists():
        raise PackageError(f"package does not exist: {path}")
    data = _manifest_from_archive(path)
    if data is None:
        raise PackageError(f"package has no readable root tul-package.yml: {path}")
    return data


def candidate_record(candidate: PackageCandidate) -> dict:
    """Return a stable, machine-readable summary for package discovery output."""
    target = candidate.manifest_data.get("target") or {}
    commit = candidate.manifest_data.get("commit") or {}
    try:
        size = candidate.source.stat().st_size
    except OSError:
        size = None
    return {
        "path": str(candidate.source),
        "name": candidate.name,
        "mtime": datetime.fromtimestamp(candidate.mtime).astimezone().isoformat(timespec="seconds"),
        "mtime_epoch": candidate.mtime,
        "size": size,
        "target": {
            "project": target.get("project"),
            "repo": target.get("repo"),
            "branch": target.get("branch"),
        },
        "commit": {
            "message": commit.get("message"),
            "files": commit.get("files") or [],
        },
        "reason": candidate.reason,
    }


def invalid_candidate_record(candidate: InvalidPackageCandidate) -> dict:
    try:
        size = candidate.source.stat().st_size
    except OSError:
        size = None
    return {
        "path": str(candidate.source),
        "name": candidate.source.stem,
        "mtime": datetime.fromtimestamp(candidate.mtime).astimezone().isoformat(timespec="seconds"),
        "mtime_epoch": candidate.mtime,
        "size": size,
        "reason": candidate.reason,
    }


def _archive_paths(global_config: dict) -> list[Path]:
    paths = platform_paths(global_config)
    archives: list[Path] = []
    for root in paths.get("inbox_roots") or []:
        if not root.exists() or not root.is_dir():
            continue
        for path in sorted(root.glob("*")):
            if path.suffix.lower() == ".zip" or path.name.lower().endswith(".tar.gz"):
                archives.append(path)
    return archives


def _target_mismatches(data: dict, *, project: str, repo: str | None, branch: str | None) -> list[str]:
    target = data.get("target") or {}
    mismatches: list[str] = []
    if str(target.get("project")) != str(project):
        mismatches.append(f"target.project={target.get('project')!r} expected {project!r}")
    if repo and str(target.get("repo")) != str(repo):
        mismatches.append(f"target.repo={target.get('repo')!r} expected {repo!r}")
    if branch and str(target.get("branch")) != str(branch):
        mismatches.append(f"target.branch={target.get('branch')!r} expected {branch!r}")
    return mismatches


def discover_package_inventory(global_config: dict, *, project: str, repo: str | None, branch: str | None) -> PackageDiscovery:
    matching: list[PackageCandidate] = []
    incompatible: list[PackageCandidate] = []
    invalid: list[InvalidPackageCandidate] = []
    for path in _archive_paths(global_config):
        try:
            mtime = path.stat().st_mtime
        except OSError:
            continue
        data = _manifest_from_archive(path)
        if not data:
            invalid.append(InvalidPackageCandidate(source=path, mtime=mtime, reason=_root_manifest_diagnostic(path)))
            continue
        mismatches = _target_mismatches(data, project=project, repo=repo, branch=branch)
        if mismatches:
            incompatible.append(PackageCandidate(source=path, manifest_data=data, mtime=mtime, reason="; ".join(mismatches)))
        else:
            matching.append(PackageCandidate(source=path, manifest_data=data, mtime=mtime, reason="target.project/repo/branch match"))
    key = lambda item: item.mtime
    return PackageDiscovery(
        matching=sorted(matching, key=key, reverse=True),
        incompatible=sorted(incompatible, key=key, reverse=True),
        invalid=sorted(invalid, key=key, reverse=True),
    )


def discover_candidates(global_config: dict, *, project: str, repo: str | None, branch: str | None) -> list[PackageCandidate]:
    return discover_package_inventory(global_config, project=project, repo=repo, branch=branch).matching


def _format_no_match_error(global_config: dict, *, project: str, repo: str | None, branch: str | None, discovery: PackageDiscovery) -> str:
    roots = platform_paths(global_config).get("inbox_roots") or []
    lines = [
        f"no matching package found for project={project!r} repo={repo!r} branch={branch!r}",
        "",
        "Inbox roots:",
    ]
    lines.extend(f"- {root}" for root in roots)
    if discovery.incompatible:
        lines.append("")
        lines.append("Found incompatible package(s):")
        for item in discovery.incompatible[:5]:
            target = item.manifest_data.get("target") or {}
            lines.append(f"- {item.source}")
            lines.append(f"  name: {item.name}")
            lines.append(f"  target: {target.get('project')} {target.get('repo')} {target.get('branch')}")
            lines.append(f"  reason: {item.reason}")
    if discovery.invalid:
        lines.append("")
        lines.append("Ignored invalid archive(s):")
        for item in discovery.invalid[:5]:
            lines.append(f"- {item.source}")
            lines.append(f"  reason: {item.reason}")
    lines.append("")
    lines.append("Options:")
    lines.append("- download a package whose tul-package.yml target matches this project/repo/branch")
    lines.append("- run: tul package list <project>")
    lines.append("- run: tul package inspect <package.zip>")
    lines.append("- run: tul package check <package.zip> <project>")
    lines.append("- use an explicit compatible package: tul update <package.zip>")
    return "\n".join(lines)


def select_package(global_config: dict, *, explicit: str | None, project: str, repo: str | None, branch: str | None) -> Path:
    if explicit:
        path = Path(explicit).expanduser().resolve()
        if not path.exists():
            raise PackageError(f"package does not exist: {path}")
        return path
    discovery = discover_package_inventory(global_config, project=project, repo=repo, branch=branch)
    if not discovery.matching:
        raise PackageError(_format_no_match_error(global_config, project=project, repo=repo, branch=branch, discovery=discovery))
    return discovery.matching[0].source


def import_package(source: Path, global_config: dict) -> ImportedPackage:
    paths = platform_paths(global_config)
    work_root = mkdirp(paths.get("work_root") or (Path.home() / ".cache" / "tul" / "work"))
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    package_id = f"{source.stem}-{stamp}"
    work_dir = mkdirp(work_root / package_id)
    copied = work_dir / source.name
    shutil.copy2(source, copied)
    digest = sha256_file(copied)
    (work_dir / "source.sha256").write_text(digest + "  " + copied.name + "\n", encoding="utf-8")
    extracted = mkdirp(work_dir / "extracted")
    safe_extract(copied, extracted)
    manifest = load_manifest(extracted / "tul-package.yml")
    return ImportedPackage(source=copied, work_dir=work_dir, extracted_dir=extracted, manifest=manifest, sha256=digest)


def safe_extract(archive: Path, dest: Path) -> None:
    dest = dest.resolve()
    mkdirp(dest)
    if zipfile.is_zipfile(archive):
        with zipfile.ZipFile(archive) as zf:
            for member in zf.infolist():
                _validate_archive_member(dest, member.filename)
            zf.extractall(dest)
        return
    if tarfile.is_tarfile(archive):
        with tarfile.open(archive) as tf:
            for member in tf.getmembers():
                _validate_archive_member(dest, member.name)
            tf.extractall(dest)
        return
    raise PackageError(f"unsupported package archive: {archive}")


def _validate_archive_member(dest: Path, name: str) -> None:
    raw = name.replace("\\", "/")
    if raw.startswith("/") or raw.startswith("~/") or (len(raw) >= 2 and raw[1] == ":"):
        raise SafetyError(f"archive member uses absolute path: {name}")
    candidate = safe_join(dest, raw)
    ensure_inside(dest, candidate)
