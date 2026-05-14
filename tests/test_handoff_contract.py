from __future__ import annotations

import unittest

from helpers import run_tul


EXPECTED_READ_NEXT = [
    "README.md",
    "docs/status/current.md",
    "docs/manifest.md",
    "docs/roadmap.md",
    "docs/commands.md",
    "docs/package-spec.md",
]

RETIRED_POINTERS = [
    "docs/llm/",
    "docs/protocols/",
    "docs/checklists/",
    "docs/workflows/",
    "docs/experiments/",
    "docs/tracks/",
    "docs/handoff.md",
    "docs/windows-dwork-environment.md",
    "templates/llm-initial-review-prompt.md",
    "templates/llm-post-update-review-prompt.md",
    "templates/project-harness/",
]


class HandoffContractTest(unittest.TestCase):
    def test_read_next_is_compact_active_set(self) -> None:
        output = run_tul("show", "handoff").stdout
        self.assertIn("## Read next", output)
        self.assertIn("## LLM task", output)
        block = output.split("## Read next", 1)[1].split("## LLM task", 1)[0]
        read_next = [line[2:].strip() for line in block.splitlines() if line.startswith("- ")]
        self.assertEqual(EXPECTED_READ_NEXT, read_next)

    def test_retired_doc_pointers_are_absent_from_handoff(self) -> None:
        output = run_tul("show", "handoff").stdout
        for retired in RETIRED_POINTERS:
            self.assertNotIn(retired, output)


if __name__ == "__main__":
    unittest.main()
