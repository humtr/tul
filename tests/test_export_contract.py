from __future__ import annotations

import unittest

from helpers import git, run_tul


class ExportContractTest(unittest.TestCase):
    def test_show_exports_reports_current_source_and_review(self) -> None:
        output = run_tul("show", "exports").stdout
        self.assertIn("## Source bundle", output)
        self.assertIn("## Review bundle", output)
        self.assertIn("- status: current", output)
        self.assertIn("## Warnings\n- none", output)

    def test_show_exports_mentions_current_head(self) -> None:
        head = git("rev-parse", "HEAD")
        output = run_tul("show", "exports").stdout
        self.assertIn(f"HEAD: {head}", output)
        self.assertIn(f"Remote HEAD: {head}", output)
        self.assertIn(f"current head: {head}", output)


if __name__ == "__main__":
    unittest.main()
