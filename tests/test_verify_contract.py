from __future__ import annotations

import sys
import unittest

from helpers import REPO_ROOT, read_text

sys.path.insert(0, str(REPO_ROOT / "lib"))

from tulcore.verify import REQUIRED_DOCS  # noqa: E402


EXPECTED_REQUIRED_DOCS = [
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


class VerifyContractTest(unittest.TestCase):
    def test_required_docs_are_active_docs_only(self) -> None:
        self.assertEqual(EXPECTED_REQUIRED_DOCS, REQUIRED_DOCS)
        for rel in REQUIRED_DOCS:
            self.assertTrue((REPO_ROOT / rel).exists(), rel)

    def test_readme_gate_terms_are_stable(self) -> None:
        text = read_text("README.md")
        for term in README_GATE_TERMS:
            self.assertIn(term, text)


if __name__ == "__main__":
    unittest.main()
