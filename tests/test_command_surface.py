from __future__ import annotations

import json
import re
import sys
import unittest

from helpers import REPO_ROOT, run_tul

sys.path.insert(0, str(REPO_ROOT / "lib"))

from tulcore.cli_parser import build_parser  # noqa: E402


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


def top_level_choices(help_output: str) -> set[str]:
    """Return parser choices from the usage line.

    This intentionally checks argparse's top-level command set rather than
    arbitrary prose in command descriptions. For example, `apply` may appear
    in the `update` description (`apply, commit, push`) without being a
    top-level command.
    """

    match = re.search(r"\{([^}]+)\}", help_output)
    if not match:
        return set()
    return {part.strip() for part in match.group(1).split(",") if part.strip()}


class CommandSurfaceTest(unittest.TestCase):
    def test_help_lists_canonical_commands(self) -> None:
        output = run_tul("help").stdout
        choices = top_level_choices(output)
        self.assertTrue(choices, "could not parse argparse top-level choices")
        for command in CANONICAL_COMMANDS:
            self.assertIn(command, choices)

    def test_removed_top_level_commands_are_not_help_entries(self) -> None:
        output = run_tul("help").stdout
        choices = top_level_choices(output)
        self.assertTrue(choices, "could not parse argparse top-level choices")
        for command in REMOVED_TOP_LEVEL_COMMANDS:
            self.assertNotIn(command, choices)
            self.assertIsNone(
                re.search(rf"^    {re.escape(command)}\s", output, re.MULTILINE),
                f"{command!r} appears as a top-level help entry",
            )


    def test_parser_builder_exposes_canonical_choices(self) -> None:
        parser = build_parser()
        output = parser.format_help()
        choices = top_level_choices(output)
        self.assertEqual(set(CANONICAL_COMMANDS + ["help"]), choices)

    def test_export_namespace_rejects_status(self) -> None:
        result = run_tul("export", "status", check=False)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("status", result.stdout.lower())

    def test_run_dry_json_is_machine_readable(self) -> None:
        result = run_tul("run", "--json", "dry")
        payload = json.loads(result.stdout)
        self.assertEqual("run", payload["command"])
        self.assertTrue(payload["dry"])
        self.assertEqual(0, payload["exit_code"])
        self.assertTrue(payload["ok"])
        self.assertIn("# tul run dry", payload["output"])


if __name__ == "__main__":
    unittest.main()
