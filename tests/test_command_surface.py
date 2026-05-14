from __future__ import annotations

import unittest

from helpers import run_tul


CANONICAL_COMMANDS = [
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


class CommandSurfaceTest(unittest.TestCase):
    def test_help_lists_canonical_commands(self) -> None:
        output = run_tul("help").stdout
        for command in CANONICAL_COMMANDS:
            self.assertIn(command, output)

    def test_removed_top_level_commands_are_not_help_entries(self) -> None:
        output = run_tul("help").stdout
        for command in REMOVED_TOP_LEVEL_COMMANDS:
            self.assertNotIn(f"  {command}", output)

    def test_export_namespace_rejects_status(self) -> None:
        result = run_tul("export", "status", check=False)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("status", result.stdout.lower())


if __name__ == "__main__":
    unittest.main()
