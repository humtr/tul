from __future__ import annotations

import unittest

from helpers import git, run_tul


class ExportContractTest(unittest.TestCase):
    def test_show_exports_reports_contract_sections_without_requiring_local_artifacts(self) -> None:
        output = run_tul("show", "exports").stdout
        self.assertIn("# tul show exports", output)
        self.assertIn("Mode: warning-only", output)
        self.assertIn("Release gate effect: none", output)
        self.assertIn("## Source bundle", output)
        self.assertIn("## Review bundle", output)
        self.assertIn("## Docs drift", output)
        self.assertIn("## Warnings", output)

    def test_show_exports_mentions_current_head(self) -> None:
        head = git("rev-parse", "HEAD")
        output = run_tul("show", "exports").stdout
        self.assertIn(f"HEAD: {head}", output)
        self.assertIn(f"Remote HEAD: {head}", output)
        self.assertIn(f"current head: {head}", output)


if __name__ == "__main__":
    unittest.main()
