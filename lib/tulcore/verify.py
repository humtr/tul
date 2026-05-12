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
from .paths import expand_path, mkdirp


REQUIRED_DOCS = [
    "README.md",
    ".tul.yml",
    "docs/llm/entrypoint.md",
    "docs/status/current.md",
    "docs/roadmap.md",
    "docs/checklists/loop-runtime.md",
    "docs/protocols/command-grammar.md",
    "docs/protocols/llm-handoff-protocol.md",
]


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

    def to_text(self) -> str:
        lines = ["# tul verify", "", f"Project: {self.project}", f"Repo: {self.repo}"]
        if self.branch:
            lines.append(f"Branch: {self.branch}")
        if self.head:
            lines.append(f"HEAD: {self.head}")
        if self.remote_head:
            lines.append(f"Remote HEAD: {self.remote_head}")
        if self.clone_path:
            lines.append(f"Fresh clone: {self.clone_path}")
        lines.append(f"Result: {'pass' if self.ok else 'fail'}")
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
    """Return the directory for persisted verify artifacts.

    Termux defaults to `/sdcard/termux/import/tul/logs/verify` by deriving the
    log root from the configured work root `/sdcard/termux/import/tul/work`.
    Windows derives `D:/work/files/downloads/.tul/logs/verify` from the work
    root unless `platform.verify_log_root` or `platform.log_root` is configured.
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


def write_verify_artifacts(
    ctx: ProjectContext,
    result: VerifyResult,
    *,
    fresh_clone: bool = False,
    log_dir: Path | None = None,
) -> dict[str, str]:
    """Persist verify output as timestamped markdown and JSON artifacts.

    Also writes stable `latest` copies so the user can upload one predictable
    file instead of copying long terminal output.
    """
    root = verify_log_root(ctx, log_dir)
    mkdirp(root)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    mode = "fresh" if fresh_clone else "local"
    head_short = (result.head or "unknown")[:12]
    stem = f"{ctx.project_id}-verify-{mode}-{stamp}-{head_short}"
    md_path = root / f"{stem}.md"
    json_path = root / f"{stem}.json"
    latest_md = root / f"{ctx.project_id}-verify-latest.md"
    latest_json = root / f"{ctx.project_id}-verify-latest.json"

    payload = result.to_dict()
    payload["artifact"] = {
        "mode": mode,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "log_root": str(root),
        "markdown": str(md_path),
        "json": str(json_path),
        "latest_markdown": str(latest_md),
        "latest_json": str(latest_json),
    }

    text = result.to_text()
    text += "\n\n## Artifact metadata\n"
    text += f"- Mode: {mode}\n"
    text += f"- Markdown: {md_path}\n"
    text += f"- JSON: {json_path}\n"
    text += f"- Latest markdown: {latest_md}\n"
    text += f"- Latest JSON: {latest_json}\n"
    text += "\n## Machine-readable summary\n\n```json\n"
    text += json.dumps(payload, indent=2, ensure_ascii=False)
    text += "\n```\n"

    md_path.write_text(text, encoding="utf-8", newline="\n")
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    latest_md.write_text(text, encoding="utf-8", newline="\n")
    latest_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")

    return {
        "markdown": str(md_path),
        "json": str(json_path),
        "latest_markdown": str(latest_md),
        "latest_json": str(latest_json),
    }


def format_verify_artifacts(paths: dict[str, str]) -> str:
    return "\n".join(
        [
            "## Verify artifacts",
            f"- Log: {paths['markdown']}",
            f"- JSON: {paths['json']}",
            f"- Latest log: {paths['latest_markdown']}",
            f"- Latest JSON: {paths['latest_json']}",
        ]
    )


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

    missing = [rel for rel in REQUIRED_DOCS if not (repo / rel).exists()]
    result.add(f"{label}: required repo docs", not missing, "missing: " + ", ".join(missing) if missing else "all present")

    readme = repo / "README.md"
    if readme.exists():
        text = readme.read_text(encoding="utf-8", errors="replace")
        required = ["LLM entrypoint", "tul update <project>", "--latest", "git add -A", "tul-package.yml + files/ + README.md"]
        missing_terms = [term for term in required if term not in text]
        result.add(f"{label}: README entrypoint terms", not missing_terms, "missing: " + ", ".join(missing_terms) if missing_terms else "all present")


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
