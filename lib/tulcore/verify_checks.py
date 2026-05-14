"""Release-gate contract checks used by `tul verify`.

These helpers keep the durable release-gate checks separate from artifact
rendering and fresh-clone orchestration in `verify.py`.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Any


REQUIRED_DOCS = [
    "README.md",
    ".tul.yml",
    "docs/status/current.md",
    "docs/manifest.md",
    "docs/roadmap.md",
    "docs/commands.md",
    "docs/package-spec.md",
]

README_GATE_TERMS = [
    "LLM entrypoint",
    "tul run",
    "tul update",
    "git add -A",
    "tul-package.yml + files/ + README.md",
]

CANONICAL_TOP_LEVEL_COMMANDS = [
    "show",
    "package",
    "update",
    "verify",
    "export",
    "run",
    "clean",
    "recover",
    "setup",
]

REMOVED_TOP_LEVEL_COMMANDS = [
    "status",
    "state",
    "report",
    "handoff",
    "instructions",
    "current",
    "projects",
    "doctor",
    "check",
    "sync",
    "publish",
    "import",
    "apply",
    "resume",
    "rollback",
    "archive",
    "sweep",
    "init",
    "install",
    "use",
    "config",
]

RUN_FALLBACK_MARKERS = [
    "No matching package found. Refreshing verification and transport artifacts for the current HEAD.",
    "Would skip update and refresh artifacts for the current HEAD.",
    "Would then run: tul verify fresh",
    "Would then run: tul show",
]


class StepRecorderProtocol:
    """Structural protocol for VerifyResult without importing verify.py."""

    def add(self, name: str, ok: bool, detail: str = "", command: str | None = None) -> None:  # pragma: no cover - protocol only
        raise NotImplementedError


def check_required_docs(repo: Path, result: StepRecorderProtocol, *, label: str) -> None:
    missing = [rel for rel in REQUIRED_DOCS if not (repo / rel).exists()]
    result.add(
        f"{label}: required repo docs",
        not missing,
        "missing: " + ", ".join(missing) if missing else "all present",
    )


def check_readme_entrypoint_terms(repo: Path, result: StepRecorderProtocol, *, label: str) -> None:
    readme = repo / "README.md"
    if not readme.exists():
        # The required-docs check reports the missing README. Avoid a duplicate
        # failure that would hide the more precise missing-docs message.
        return
    text = readme.read_text(encoding="utf-8", errors="replace")
    missing_terms = [term for term in README_GATE_TERMS if term not in text]
    result.add(
        f"{label}: README entrypoint terms",
        not missing_terms,
        "missing: " + ", ".join(missing_terms) if missing_terms else "all present",
    )


def check_command_surface(repo: Path, result: StepRecorderProtocol, *, label: str) -> None:
    """Smoke-test the canonical command surface without project config.

    These checks intentionally avoid commands such as `tul show` or `tul run`
    that may require a configured project. They verify the parser/help surface,
    removed top-level command rejection, `export` namespace purity, and the
    static `run` fallback markers that define the package-not-found refresh
    path.
    """
    launcher = repo / "bin" / "tul"
    if not launcher.exists():
        result.add(f"{label}: command surface launcher", False, "missing: bin/tul")
        return

    help_proc = subprocess.run(
        [sys.executable, str(launcher), "help"],
        cwd=str(repo),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    help_text = help_proc.stdout + help_proc.stderr
    missing = [cmd for cmd in CANONICAL_TOP_LEVEL_COMMANDS if cmd not in help_text]
    result.add(
        f"{label}: command surface help",
        help_proc.returncode == 0 and not missing,
        "missing: " + ", ".join(missing) if missing else "canonical commands present",
        command=f"{sys.executable} bin/tul help",
    )

    cli = repo / "lib" / "tulcore" / "cli_parser.py"
    if not cli.exists():
        result.add(f"{label}: removed top-level parser entries absent", False, "missing: lib/tulcore/cli_parser.py")
        cli_text = ""
    else:
        cli_text = cli.read_text(encoding="utf-8", errors="replace")
        parser_entries = [command for command in REMOVED_TOP_LEVEL_COMMANDS if f'sub.add_parser("{command}"' in cli_text]
        help_leaks = [
            command for command in REMOVED_TOP_LEVEL_COMMANDS
            if f"  {command} " in help_text or f"{{{command}," in help_text or f",{command}," in help_text
        ]
        leaks = sorted(set(parser_entries + help_leaks))
        result.add(
            f"{label}: removed top-level parser entries absent",
            not leaks,
            "unexpectedly present: " + ", ".join(leaks) if leaks else "removed commands absent from parser/help",
        )

    export_status = subprocess.run(
        [sys.executable, str(launcher), "export", "status"],
        cwd=str(repo),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    result.add(
        f"{label}: export namespace file-producing only",
        export_status.returncode != 0,
        "export status rejected" if export_status.returncode != 0 else "export status unexpectedly accepted",
        command=f"{sys.executable} bin/tul export status",
    )

    if not cli_text:
        result.add(f"{label}: run fallback markers", False, "missing: lib/tulcore/cli_parser.py")
        return
    # The fallback behavior lives in cli.py command_run, not in cli_parser.py.
    cli_runtime = repo / "lib" / "tulcore" / "cli.py"
    runtime_text = cli_runtime.read_text(encoding="utf-8", errors="replace") if cli_runtime.exists() else ""
    missing_markers = [marker for marker in RUN_FALLBACK_MARKERS if marker not in runtime_text]
    result.add(
        f"{label}: run fallback markers",
        not missing_markers,
        "missing: " + "; ".join(missing_markers) if missing_markers else "package-not-found refresh markers present",
    )
