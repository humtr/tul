"""Verification helpers for tul repos and optional fresh clones."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from .config import ProjectContext, platform_paths
from .gitops import remote_url
from .handoff import generate_handoff
from .integrity import format_export_integrity
from .paths import expand_path, mkdirp
from .state import latest_state, summarize_compact_state
from .upload_aliases import publish_verify_upload_alias, remove_root_latest_artifacts
from .verify_checks import (
    REQUIRED_DOCS,
    check_cli_runtime_smoke,
    check_command_surface,
    check_readme_entrypoint_terms,
    check_regression_tests,
    check_required_docs,
)


@dataclass
class VerifyStep:
    name: str
    ok: bool
    detail: str = ""
    command: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {"name": self.name, "ok": self.ok, "detail": self.detail, "command": self.command}


@dataclass
class VerifyResult:
    project: str
    repo: str
    branch: str | None = None
    head: str | None = None
    remote_head: str | None = None
    clone_path: str | None = None
    steps: list[VerifyStep] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return all(step.ok for step in self.steps)

    def add(self, name: str, ok: bool, detail: str = "", command: str | None = None) -> None:
        self.steps.append(VerifyStep(name=name, ok=ok, detail=detail, command=command))

    def to_dict(self) -> dict[str, Any]:
        return {
            "project": self.project,
            "repo": self.repo,
            "branch": self.branch,
            "head": self.head,
            "remote_head": self.remote_head,
            "clone_path": self.clone_path,
            "ok": self.ok,
            "steps": [step.to_dict() for step in self.steps],
        }

    def step_counts(self) -> tuple[int, int]:
        failed = sum(1 for step in self.steps if not step.ok)
        return len(self.steps) - failed, failed

    def to_text(self, artifacts: dict[str, str] | None = None) -> str:
        passed, failed = self.step_counts()
        lines = [
            "# tul verify",
            "",
            f"Release gate: {'PASS' if self.ok else 'FAIL'}",
            "",
            f"Project: {self.project}",
            f"Repo: {self.repo}",
        ]
        if self.branch:
            lines.append(f"Branch: {self.branch}")
        if self.head:
            lines.append(f"HEAD: {self.head}")
        if self.remote_head:
            lines.append(f"Remote HEAD: {self.remote_head}")
        if self.clone_path:
            lines.append(f"Fresh clone: {self.clone_path}")
        lines.append(f"Steps: {passed} pass, {failed} fail")
        lines.append(f"Result: {'pass' if self.ok else 'fail'}")
        if artifacts:
            lines.extend(["", format_verify_artifacts(artifacts)])
        lines.append("")
        lines.append("## Steps")
        for step in self.steps:
            mark = "PASS" if step.ok else "FAIL"
            lines.append(f"- [{mark}] {step.name}")
            if step.command:
                lines.append(f"  command: {step.command}")
            if step.detail:
                for line in str(step.detail).splitlines():
                    lines.append(f"  {line}")
        return "\n".join(lines)


def run_verify(ctx: ProjectContext, *, fresh_clone: bool = False, clone_root: Path | None = None) -> VerifyResult:
    repo = ctx.repo_path
    result = VerifyResult(project=ctx.project_id, repo=str(repo))
    _verify_repo(repo, result, label="local repo")
    if fresh_clone:
        clone_path = _fresh_clone_path(ctx, clone_root)
        result.clone_path = str(clone_path)
        ok, detail = _clone_remote(ctx, clone_path)
        result.add("fresh clone", ok, detail, command=f"git clone {_clone_url(ctx)} {clone_path}")
        if ok:
            _verify_repo(clone_path, result, label="fresh clone")
    return result


def verify_log_root(ctx: ProjectContext, explicit: Path | None = None) -> Path:
    """Return the directory for timestamped verify run artifacts.

    Termux defaults to `/sdcard/termux/import/tul/logs/verify` by deriving the
    log root from the configured work root `/sdcard/termux/import/tul/work`.
    Windows derives `D:/work/files/downloads/.tul/logs/verify` from the work
    root unless `platform.verify_log_root` or `platform.log_root` is configured.

    Head-tagged upload markdown is written outside this run-log root by
    `verify_upload_root()`, so the import root can hold the three canonical
    upload artifacts. Verify does not create `tul-main.zip` or any other
    source archive.
    """
    if explicit is not None:
        return explicit.expanduser().resolve()
    platform = ctx.global_config.get("platform") or {}
    if platform.get("verify_log_root"):
        return expand_path(str(platform["verify_log_root"]))
    if platform.get("log_root"):
        return expand_path(str(platform["log_root"])) / "verify"
    paths = platform_paths(ctx.global_config)
    work_root = paths.get("work_root")
    if work_root:
        return Path(work_root).parent / "logs" / "verify"
    return Path.home() / ".cache" / "tul" / "logs" / "verify"


def verify_upload_root(ctx: ProjectContext, log_root: Path) -> Path:
    """Return the import root used for canonical head-tagged upload artifacts.

    Timestamped run artifacts remain in `logs/verify/YYMMDD/`. The root uses
    head-tagged names only; latest-named verify artifacts are not generated.
    """
    platform = ctx.global_config.get("platform") or {}
    if platform.get("verify_upload_root"):
        return expand_path(str(platform["verify_upload_root"]))
    paths = platform_paths(ctx.global_config)
    work_root = paths.get("work_root")
    if work_root:
        return Path(work_root).parent
    # Best-effort fallback for explicit/default log roots that end in logs/verify.
    if log_root.name == "verify" and log_root.parent.name == "logs":
        return log_root.parent.parent
    return log_root


def write_verify_artifacts(
    ctx: ProjectContext,
    result: VerifyResult,
    *,
    fresh_clone: bool = False,
    log_dir: Path | None = None,
    include_runtime_snapshots: bool = True,
) -> dict[str, str]:
    """Persist verify output as canonical markdown and JSON artifacts.

    Timestamped run artifacts are stored under the verify run-log root in a
    YYMMDD date folder. Head-tagged markdown aliases are written to the import root for upload.
    Machine-readable JSON is kept in dated logs, not as a root latest file.
    Latest-named artifacts are intentionally not generated.
    """
    log_root = verify_log_root(ctx, log_dir)
    upload_root = verify_upload_root(ctx, log_root)
    mkdirp(log_root)
    mkdirp(upload_root)
    now = datetime.now()
    date_key = now.strftime("%y%m%d")
    time_key = now.strftime("%H%M%S")
    mode = "fresh" if fresh_clone else "local"
    mode_key = "f" if fresh_clone else "l"
    head_short = (result.head or "unknown")[:7]

    run_root = mkdirp(log_root / date_key)
    stem = f"{ctx.project_id}-vf-{mode_key}-{date_key}-{time_key}-{head_short}"
    md_path = run_root / f"{stem}.md"
    json_path = run_root / f"{stem}.json"
    root_verify_md = upload_root / f"{ctx.project_id}-vf-{head_short}.md"

    payload = result.to_dict()
    payload["artifact"] = {
        "mode": mode,
        "created_at": now.isoformat(timespec="seconds"),
        "log_root": str(log_root),
        "run_root": str(run_root),
        "upload_root": str(upload_root),
        "markdown": str(md_path),
        "json": str(json_path),
        "upload_markdown": str(root_verify_md),
    }

    artifacts = {
        "markdown": str(md_path),
        "json": str(json_path),
        "upload_markdown": str(root_verify_md),
    }
    text = render_verify_artifact_markdown(
        ctx,
        result,
        artifacts,
        payload,
        include_runtime_snapshots=include_runtime_snapshots,
    )

    md_path.write_text(text, encoding="utf-8", newline="\n")
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    alias = publish_verify_upload_alias(ctx, md_path, json_path=json_path, head=result.head).to_dict()
    alias_map = _merged_upload_aliases(ctx, verify_alias=alias)
    payload["artifact"]["upload_aliases"] = alias_map
    artifacts["upload_source"] = str((alias_map.get("source") or {}).get("root_alias") or "")
    artifacts["upload_review"] = str((alias_map.get("review") or {}).get("root_alias") or "")
    artifacts["upload_markdown"] = alias.get("root_alias", "")
    artifacts["upload_dated_markdown"] = alias.get("dated_alias", "")

    text = render_verify_artifact_markdown(
        ctx,
        result,
        artifacts,
        payload,
        include_runtime_snapshots=include_runtime_snapshots,
    )
    md_path.write_text(text, encoding="utf-8", newline="\n")
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    # Refresh the root upload markdown from the final rendered content and keep
    # machine-readable JSON only in the dated verify log.
    Path(artifacts["upload_markdown"]).write_text(text, encoding="utf-8", newline="\n")
    removed_latest = remove_root_latest_artifacts(ctx, kinds=("vf",))
    if removed_latest:
        payload.setdefault("artifact", {}).setdefault("upload_aliases", {}).setdefault("verify", {})["removed_latest"] = removed_latest
        json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    return artifacts


def rewrite_verify_artifacts_with_runtime_snapshots(
    ctx: ProjectContext,
    result: VerifyResult,
    artifacts: dict[str, str],
) -> None:
    """Rewrite existing verify markdown/upload alias with state/handoff snapshots.

    `tul update` runs the fresh verification gate before it writes the final
    handoff-ready state and handoff files. This helper is called after those
    files exist, so the head-tagged verify markdown can serve as the single
    upload artifact for release gate, compact state, and compact handoff evidence.
    """
    json_path = Path(artifacts["json"])
    if json_path.exists():
        payload = json.loads(json_path.read_text(encoding="utf-8"))
    else:
        payload = result.to_dict()
    json_path_obj = Path(artifacts.get("json", "")) if artifacts.get("json") else None
    md_path_obj = Path(artifacts["markdown"])
    verify_alias = publish_verify_upload_alias(
        ctx,
        md_path_obj,
        json_path=json_path_obj if json_path_obj and json_path_obj.exists() else None,
        head=result.head,
    ).to_dict()
    alias_map = _merged_upload_aliases(ctx, verify_alias=verify_alias)
    payload.setdefault("artifact", {})["upload_aliases"] = alias_map
    artifacts["upload_source"] = str((alias_map.get("source") or {}).get("root_alias") or "")
    artifacts["upload_review"] = str((alias_map.get("review") or {}).get("root_alias") or "")
    artifacts["upload_markdown"] = verify_alias.get("root_alias", "")
    if json_path_obj and json_path_obj.exists():
        json_path_obj.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    text = render_verify_artifact_markdown(
        ctx,
        result,
        artifacts,
        payload,
        include_runtime_snapshots=True,
    )
    Path(artifacts["markdown"]).write_text(text, encoding="utf-8", newline="\n")
    if artifacts.get("upload_markdown"):
        Path(artifacts["upload_markdown"]).write_text(text, encoding="utf-8", newline="\n")
    remove_root_latest_artifacts(ctx, kinds=("vf",))



def refresh_verify_upload_runtime_snapshots(ctx: ProjectContext) -> bool:
    """Refresh head-tagged verify upload aliases when possible.

    The dated run artifact remains the durable verify record. The root upload
    surface is head-tagged only, so no latest-named file is refreshed.
    """
    remove_root_latest_artifacts(ctx, kinds=("vf",))
    return False


def _merged_upload_aliases(ctx: ProjectContext, *, verify_alias: dict[str, Any]) -> dict[str, Any]:
    aliases: dict[str, Any] = {}
    state_aliases = _transport_upload_aliases_from_latest_state(ctx)
    aliases.update(state_aliases)
    aliases["verify"] = verify_alias
    return aliases


def _transport_upload_aliases_from_latest_state(ctx: ProjectContext) -> dict[str, Any]:
    paths = platform_paths(ctx.global_config)
    work_root = paths.get("work_root")
    if not work_root:
        return {}
    found = latest_state(Path(work_root), project=ctx.project_id)
    if not found:
        return {}
    _, data = found
    aliases: dict[str, Any] = {}
    for key, label in (("source_bundle_export", "source"), ("review_bundle_export", "review")):
        export = data.get(key)
        if isinstance(export, dict):
            upload_aliases = export.get("upload_aliases")
            if isinstance(upload_aliases, dict) and upload_aliases.get("root_alias"):
                aliases[label] = upload_aliases
    post = data.get("post_update_exports")
    if isinstance(post, dict):
        for label in ("source", "review"):
            item = post.get(label)
            if isinstance(item, dict):
                upload_aliases = item.get("upload_aliases")
                if isinstance(upload_aliases, dict) and upload_aliases.get("root_alias"):
                    aliases[label] = upload_aliases
    return aliases

def _verify_result_from_payload(payload: dict[str, Any]) -> VerifyResult:
    result = VerifyResult(
        project=str(payload.get("project") or "unknown"),
        repo=str(payload.get("repo") or "unknown"),
        branch=payload.get("branch"),
        head=payload.get("head"),
        remote_head=payload.get("remote_head"),
        clone_path=payload.get("clone_path"),
    )
    for item in payload.get("steps") or []:
        if not isinstance(item, dict):
            continue
        result.steps.append(VerifyStep(
            name=str(item.get("name") or "step"),
            ok=bool(item.get("ok")),
            detail=str(item.get("detail") or ""),
            command=item.get("command"),
        ))
    return result

def render_verify_artifact_markdown(
    ctx: ProjectContext,
    result: VerifyResult,
    artifacts: dict[str, str],
    payload: dict[str, Any],
    *,
    include_runtime_snapshots: bool = True,
) -> str:
    artifact = payload.get("artifact") if isinstance(payload.get("artifact"), dict) else {}
    text = result.to_text(artifacts)
    text += "\n\n## Artifact metadata\n"
    mode_value = artifact.get("mode") or ("fresh" if result.clone_path else "local")
    text += f"- Mode: {mode_value}\n"
    if artifact.get("log_root"):
        text += f"- Log root: {artifact['log_root']}\n"
    if artifact.get("run_root"):
        text += f"- Run root: {artifact['run_root']}\n"
    if artifact.get("upload_root"):
        text += f"- Upload root: {artifact['upload_root']}\n"
    text += f"- Run markdown: {artifacts['markdown']}\n"
    text += f"- Run JSON: {artifacts['json']}\n"
    if artifacts.get("upload_markdown"):
        text += f"- Upload markdown: {artifacts['upload_markdown']}\n"
    if include_runtime_snapshots:
        text += "\n" + format_runtime_snapshots(ctx)
    text += "\n## Machine-readable summary\n\n```json\n"
    text += json.dumps(payload, indent=2, ensure_ascii=False)
    text += "\n```\n"
    return text


def format_runtime_snapshots(ctx: ProjectContext) -> str:
    """Return compact state and handoff snapshots for verify markdown."""
    lines = [
        "## Runtime snapshots",
        "",
        "These snapshots are included so the head-tagged verify markdown can be uploaded as the canonical post-run verification artifact.",
        "",
        "### tul show",
        "",
        "~~~text",
    ]
    try:
        paths = platform_paths(ctx.global_config)
        work_root = paths.get("work_root")
        if not work_root:
            state_text = "No platform.work_root configured."
        else:
            state_text = summarize_compact_state(work_root, project=ctx.project_id)
    except Exception as exc:  # pragma: no cover - defensive artifact path
        state_text = f"Unable to capture tul show snapshot: {type(exc).__name__}: {exc}"
    lines.append(state_text.rstrip())
    lines.extend([
        "~~~",
        "",
        "### tul show handoff",
        "",
        "~~~text",
    ])
    try:
        handoff_text = generate_handoff(
            repo=ctx.repo_path,
            project=ctx.project_id,
            mode="verify-snapshot",
            expected_repo=ctx.expected_repo,
        )
    except Exception as exc:  # pragma: no cover - defensive artifact path
        handoff_text = f"Unable to capture tul show handoff snapshot: {type(exc).__name__}: {exc}"
    lines.append(handoff_text.rstrip())
    lines.extend([
        "~~~",
        "",
        "### tul show exports",
        "",
        "~~~text",
    ])
    try:
        export_text = format_export_integrity(ctx)
    except Exception as exc:  # pragma: no cover - defensive artifact path
        export_text = f"Unable to capture tul show exports snapshot: {type(exc).__name__}: {exc}"
    lines.append(export_text.rstrip())
    lines.append("~~~")
    return "\n".join(lines) + "\n"

def format_verify_artifacts(paths: dict[str, str]) -> str:
    return "\n".join(
        [
            "## Verify artifacts",
            f"- Run log: {paths['markdown']}",
            f"- Run JSON: {paths['json']}",
            *([f"- Upload source: {paths['upload_source']}"] if paths.get("upload_source") else []),
            *([f"- Upload review: {paths['upload_review']}"] if paths.get("upload_review") else []),
            *([f"- Upload markdown: {paths['upload_markdown']}"] if paths.get("upload_markdown") else []),
        ]
    )



def format_verify_gate(result: VerifyResult, artifacts: dict[str, str] | None = None) -> str:
    """Return a compact release-gate summary for update output.

    Full step details are persisted in the markdown/json artifacts; update output
    should preserve commit/push/rollback visibility while still telling the user
    whether the post-update fresh verification passed and which file to upload.
    """
    passed, failed_count = result.step_counts()
    failed = [step for step in result.steps if not step.ok]
    lines = [
        "# tul verify fresh",
        "",
        f"Release gate: {'PASS' if result.ok else 'FAIL'}",
        "",
        f"Project: {result.project}",
        f"Repo: {result.repo}",
        f"Branch: {result.branch or 'unknown'}",
        f"HEAD: {result.head or 'unknown'}",
        f"Remote HEAD: {result.remote_head or 'unknown'}",
    ]
    if result.clone_path:
        lines.append(f"Fresh clone: {result.clone_path}")
    lines.append(f"Steps: {passed} pass, {failed_count} fail")
    if failed:
        lines.extend(["", "## Failed steps"])
        for step in failed:
            lines.append(f"- {step.name}: {step.detail or 'failed'}")
    if artifacts:
        lines.extend(["", format_verify_artifacts(artifacts)])
    return "\n".join(lines) + "\n"


def _verify_repo(repo: Path, result: VerifyResult, *, label: str) -> None:
    if not repo.exists():
        result.add(f"{label}: repo exists", False, f"missing: {repo}")
        return
    result.add(f"{label}: repo exists", True, str(repo))

    ok, branch = _capture(["git", "branch", "--show-current"], cwd=repo)
    branch = branch.strip() if ok else ""
    result.branch = result.branch or branch
    result.add(f"{label}: branch", ok and bool(branch), branch or "unavailable", command="git branch --show-current")

    _run_step(result, f"{label}: fetch", ["git", "fetch", "origin", branch] if branch else ["git", "fetch", "origin"], repo)

    ok, local_head = _capture(["git", "rev-parse", "HEAD"], cwd=repo)
    local_head = local_head.strip() if ok else ""
    if label == "local repo":
        result.head = local_head or result.head
    result.add(f"{label}: HEAD", ok and bool(local_head), local_head or "unavailable", command="git rev-parse HEAD")

    remote = ""
    if branch:
        ok, remote = _capture(["git", "rev-parse", f"origin/{branch}"], cwd=repo)
        remote = remote.strip() if ok else ""
        if label == "local repo":
            result.remote_head = remote or result.remote_head
        result.add(f"{label}: remote HEAD", ok and bool(remote), remote or "unavailable", command=f"git rev-parse origin/{branch}")
        if local_head and remote:
            result.add(f"{label}: HEAD matches remote", local_head == remote, f"local={local_head}\nremote={remote}")

    ok, status = _capture(["git", "status", "--porcelain"], cwd=repo)
    status = status.rstrip() if ok else ""
    result.add(f"{label}: working tree clean", ok and status == "", status or "clean", command="git status --porcelain")

    _py_compile(result, repo, f"{label}: py_compile bin/tul", [repo / "bin" / "tul"])
    lib_files = sorted((repo / "lib" / "tulcore").glob("*.py"))
    _py_compile(result, repo, f"{label}: py_compile lib/tulcore/*.py", lib_files)

    _run_step(result, f"{label}: git diff --check", ["git", "diff", "--check"], repo)

    check_required_docs(repo, result, label=label)
    check_readme_entrypoint_terms(repo, result, label=label)
    check_command_surface(repo, result, label=label)
    if label == "local repo":
        check_cli_runtime_smoke(repo, result, label=label)
        check_regression_tests(repo, result, label=label)


def _py_compile(result: VerifyResult, repo: Path, name: str, files: list[Path]) -> None:
    if not files:
        result.add(name, False, "no files matched")
        return
    cmd = [sys.executable, "-m", "py_compile", *[str(path.relative_to(repo)) for path in files]]
    _run_step(result, name, cmd, repo)


def _run_step(result: VerifyResult, name: str, cmd: list[str], cwd: Path) -> None:
    proc = subprocess.run(cmd, cwd=str(cwd), text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    detail = (proc.stdout + proc.stderr).strip() or "ok"
    result.add(name, proc.returncode == 0, detail, command=" ".join(cmd))


def _capture(cmd: list[str], *, cwd: Path) -> tuple[bool, str]:
    proc = subprocess.run(cmd, cwd=str(cwd), text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return proc.returncode == 0, proc.stdout if proc.returncode == 0 else proc.stderr


def _clone_url(ctx: ProjectContext) -> str:
    url = remote_url(ctx.repo_path) or ""
    if url.startswith("git@github.com:"):
        slug = url[len("git@github.com:"):]
        if slug.endswith(".git"):
            slug = slug[:-4]
        return f"https://github.com/{slug}.git"
    if url.startswith("https://") or url.startswith("http://"):
        return url
    if ctx.expected_repo:
        return f"https://github.com/{ctx.expected_repo}.git"
    return url


def _fresh_clone_path(ctx: ProjectContext, clone_root: Path | None) -> Path:
    root = clone_root or (Path.home() / "tmp" / "tul-verify-fresh")
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return root / f"{ctx.project_id}-{stamp}"


def _clone_remote(ctx: ProjectContext, dest: Path) -> tuple[bool, str]:
    dest.parent.mkdir(parents=True, exist_ok=True)
    url = _clone_url(ctx)
    if not url:
        return False, "could not determine remote clone URL"
    if dest.exists():
        return False, f"destination already exists: {dest}"
    proc = subprocess.run(["git", "clone", url, str(dest)], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    detail = (proc.stdout + proc.stderr).strip() or "ok"
    return proc.returncode == 0, detail
