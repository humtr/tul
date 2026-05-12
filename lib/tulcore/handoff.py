"""LLM handoff prompt generation.

Default handoff output is intentionally compact. Durable protocol details live in
repo documents so repeated terminal handoffs do not become large instruction dumps.
Use ``tul handoff <project> --full`` when an LLM needs the full loop contract in
one terminal output.
"""
from __future__ import annotations

from pathlib import Path

from .gitops import current_branch, fetch, head, recent_commits, remote_head, remote_url, status_porcelain

INVARIANTS = [
    "tul update pushes by default; --no-push is an exception.",
    "tul update is the full-loop command, not a split-command default.",
    "Never use git add -A or git add . in the default update path.",
    "Never force-push in the normal path.",
    "Project-specific policy belongs in .tul.yml, not engine code.",
    "Environment paths belong in global config, not engine code.",
    "Windows/Termux package flow should converge on tul-package.yml + files/.",
    "Successful update must print rollback instructions and an LLM-ready handoff.",
]

DOC_POINTERS = [
    "README.md",
    "docs/llm/entrypoint.md",
    "docs/llm/post-update-review.md",
    "docs/workflows/parallel-readiness.md",
    "docs/llm/commands.md",
    "docs/llm/project-instructions.md",
    "docs/status/current.md",
    "docs/roadmap.md",
    "docs/checklists/loop-runtime.md",
    "docs/protocols/command-grammar.md",
    "docs/protocols/llm-handoff-protocol.md",
    "docs/tracks/loop-runtime.md",
    "docs/handoff.md",
]

TEMPLATE_POINTERS = [
    "templates/project-instructions.md",
    "templates/llm-initial-review-prompt.md",
    "templates/llm-post-update-review-prompt.md",
]


def repo_doc_path(repo: Path, rel: str) -> str:
    path = repo / rel
    return rel if path.exists() else f"{rel} (missing)"


def runtime_facts(
    *,
    repo: Path,
    project: str,
    mode: str,
    expected_repo: str | None = None,
    package_name: str | None = None,
    commit_hash: str | None = None,
    push_verified: bool | None = None,
    changed_files: list[str] | None = None,
    rollback_command: str | None = None,
    state_file: Path | None = None,
    report_file: Path | None = None,
    outcome: str | None = None,
    verify_fresh_ok: bool | None = None,
    verify_artifacts: dict[str, str] | None = None,
    repo_zip_export: dict[str, object] | None = None,
) -> list[str]:
    branch = current_branch(repo)
    remote = None
    try:
        fetch(repo, branch)
        remote = remote_head(repo, branch)
    except Exception:
        remote = None
    status = status_porcelain(repo)

    lines = [
        "# tul LLM handoff",
        "",
        f"Mode: {mode}",
        f"Project: {project}",
        f"Repo path: {repo}",
        f"Repo URL: {remote_url(repo) or 'unknown'}",
        f"Expected repo: {expected_repo or 'unknown'}",
        f"Branch: {branch}",
        f"HEAD: {head(repo)}",
        f"Remote HEAD after fetch: {remote or 'unavailable'}",
        f"Working tree: {'clean' if not status else 'dirty'}",
        f"Active package: {package_name or 'none'}",
    ]
    if outcome:
        lines.append(f"Outcome: {outcome}")
    if commit_hash:
        lines.append(f"Commit hash: {commit_hash}")
    if outcome == "noop":
        lines.append("Push verified: not applicable for no-op")
    elif push_verified is not None:
        lines.append(f"Push verified: {str(push_verified).lower()}")
    else:
        lines.append("Push verified: not available for this session")
    if rollback_command:
        lines.append(f"Rollback command: {rollback_command}")
    if state_file:
        lines.append(f"State file: {state_file}")
    if report_file:
        lines.append(f"Report file: {report_file}")
    if verify_fresh_ok is not None:
        lines.append(f"Verify fresh: {'PASS' if verify_fresh_ok else 'FAIL'}")
    if verify_artifacts:
        latest_md = verify_artifacts.get("latest_markdown")
        md = verify_artifacts.get("markdown")
        if latest_md:
            lines.append(f"Verify latest markdown: {latest_md}")
        if md:
            lines.append(f"Verify timestamped markdown: {md}")
    if changed_files is not None:
        lines.extend(["", "## Changed files"])
        if changed_files:
            lines.extend(f"- {item}" for item in changed_files)
        else:
            lines.append("- none")
    return lines


def compact_handoff(*, repo: Path, project: str, mode: str, expected_repo: str | None, **kwargs) -> str:
    lines = runtime_facts(repo=repo, project=project, mode=mode, expected_repo=expected_repo, **kwargs)
    lines.extend([
        "",
        "## Read next",
        "",
    ])
    lines.extend(f"- {repo_doc_path(repo, rel)}" for rel in DOC_POINTERS)
    lines.extend([
        "",
        "## LLM task",
        "",
        "1. Verify remote repo, branch, HEAD, and working tree facts when remote access is available.",
        "2. Read `docs/llm/entrypoint.md`, `docs/llm/post-update-review.md`, and `docs/workflows/parallel-readiness.md` before proposing the next package.",
        "3. Treat `tul-vf-latest.md`, `tul state`, and handoff output as runtime facts; treat repo docs as durable guidance.",
        "4. Preserve push-by-default, no broad staging, no force push, and config/policy separation.",
        "5. Check bundle overlap and serialize work when files or acceptance gates conflict.",
        "6. For next work, propose or produce one cross-platform `tul-package.yml + files/ + README.md` package.",
        "",
        "For the full protocol, run:",
        "",
        f"```bash\ntul handoff {project} --full\n```",
    ])
    return "\n".join(lines) + "\n"


def full_handoff(*, repo: Path, project: str, mode: str, expected_repo: str | None, validation: list[str] | None = None, **kwargs) -> str:
    lines = runtime_facts(repo=repo, project=project, mode=mode, expected_repo=expected_repo, **kwargs)
    if validation:
        lines.extend(["", "## Validation results"])
        for item in validation:
            lines.append(f"- {item.splitlines()[0] if item else 'check'}")
    lines.extend(["", "## Recent commits", ""])
    lines.extend(f"- {item}" for item in recent_commits(repo))
    lines.extend(["", "## Track / invariants", ""])
    lines.extend(f"- {item}" for item in INVARIANTS)
    lines.extend(["", "## Repo-resident loop documents", ""])
    lines.extend(f"- {repo_doc_path(repo, rel)}" for rel in DOC_POINTERS)
    lines.extend(["", "## Prompt templates", ""])
    lines.extend(f"- {repo_doc_path(repo, rel)}" for rel in TEMPLATE_POINTERS)
    lines.extend([
        "",
        "## LLM-side command grammar",
        "",
        "- `/tul next <project>`: read the repo and propose the next implementation package scope.",
        "- `/tul review <project>`: review the just-pushed commit and handoff.",
        "- `/tul package <project>`: produce a cross-platform tul package for the next accepted scope.",
        "- `/tul roadmap <project>`: update roadmap/status/checklist documents.",
        "- `/tul verify <project>`: verify repo state against handoff/protocol/roadmap.",
        "- `/tul init-review <project>`: perform initial review after clone/init.",
        "",
        "## Request to LLM",
        "",
        "1. Treat this handoff as a structured remote-review request.",
        "2. Verify remote repo, branch, and expected HEAD when possible.",
        "3. If remote verification is unavailable, say so explicitly.",
        "4. Read `docs/llm/entrypoint.md`, `docs/llm/post-update-review.md`, `docs/workflows/parallel-readiness.md`, `docs/status/current.md`, and `docs/roadmap.md` before proposing implementation.",
        "5. Compare terminal-verified facts against remote state and the latest verify artifact.",
        "6. Identify structural debt, missing automation, and next package boundary.",
        "7. Preserve all tul invariants and do not regress push-by-default semantics.",
        "8. If generating files, produce a cross-platform `tul-package.yml + files/ + README.md` package.",
        "",
        "## Source separation",
        "",
        "사용자가 직접 말한 것:",
        "- tul은 Windows/Termux/LLM 사이의 폐루프 도구여야 한다.",
        "- tul update는 push, remote verification, rollback 안내, handoff 출력을 포함해야 한다.",
        "",
        "terminal-verified facts:",
        f"- Local HEAD at handoff generation: {head(repo)}",
        "- Remote HEAD after fetch is shown above.",
        "- Working tree status is shown above.",
        "",
        "assistant interpretation:",
        "- Treat compact handoff as runtime fact + document pointer, not as the full contract.",
        "",
        "불확실하거나 확인 필요한 부분:",
        "- Remote file contents must be re-read by the receiving LLM if repository access is available.",
    ])
    return "\n".join(lines) + "\n"


def generate_handoff(
    *,
    repo: Path,
    project: str,
    mode: str,
    expected_repo: str | None = None,
    package_name: str | None = None,
    commit_hash: str | None = None,
    push_verified: bool | None = None,
    changed_files: list[str] | None = None,
    validation: list[str] | None = None,
    rollback_command: str | None = None,
    state_file: Path | None = None,
    report_file: Path | None = None,
    outcome: str | None = None,
    verify_fresh_ok: bool | None = None,
    verify_artifacts: dict[str, str] | None = None,
    repo_zip_export: dict[str, object] | None = None,
    full: bool = False,
) -> str:
    kwargs = dict(
        package_name=package_name,
        commit_hash=commit_hash,
        push_verified=push_verified,
        changed_files=changed_files,
        rollback_command=rollback_command,
        state_file=state_file,
        report_file=report_file,
        outcome=outcome,
        verify_fresh_ok=verify_fresh_ok,
        verify_artifacts=verify_artifacts,
        repo_zip_export=repo_zip_export,
    )
    if full:
        return full_handoff(
            repo=repo,
            project=project,
            mode=mode,
            expected_repo=expected_repo,
            validation=validation,
            **kwargs,
        )
    return compact_handoff(repo=repo, project=project, mode=mode, expected_repo=expected_repo, **kwargs)
