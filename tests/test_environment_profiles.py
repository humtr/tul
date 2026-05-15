from __future__ import annotations

import unittest

from helpers import REPO_ROOT


class EnvironmentProfileTest(unittest.TestCase):
    def test_termux_tmp_policy_uses_home_tmp(self) -> None:
        text = (REPO_ROOT / "docs/environments/README.md").read_text(encoding="utf-8")
        self.assertIn("# Profile: termux-local", text)
        termux_block = text.split("# Profile: termux-local", 1)[1].split("# Profile: windows-dwork", 1)[0]

        self.assertIn("~/tmp", termux_block)
        self.assertIn("~/tmp/tul-verify-fresh", termux_block)
        self.assertIn("~/tmp/tul-backups", termux_block)
        self.assertIn("Do not use `/tmp`", termux_block)

    def test_termux_tmp_policy_matches_runtime_defaults(self) -> None:
        parser_text = (REPO_ROOT / "lib/tulcore/cli_parser.py").read_text(encoding="utf-8")
        platform_text = (REPO_ROOT / "lib/tulcore/platform.py").read_text(encoding="utf-8")
        verify_text = (REPO_ROOT / "lib/tulcore/verify.py").read_text(encoding="utf-8")

        self.assertIn("~/tmp/tul-verify-fresh", parser_text)
        self.assertIn('"backup_root": "~/tmp/tul-backups"', platform_text)
        self.assertIn('Path.home() / "tmp" / "tul-verify-fresh"', verify_text)


if __name__ == "__main__":
    unittest.main()
