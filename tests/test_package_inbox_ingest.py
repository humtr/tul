from __future__ import annotations

import tempfile
import unittest
import zipfile
from pathlib import Path

from lib.tulcore.package import import_package


def write_package(path: Path) -> None:
    manifest = """version: 1
name: sample-package

target:
  project: tul
  repo: humtr/tul
  branch: main

apply:
  mode: copy
  files:
    - from: files/README.md
      to: README.md

commit:
  files:
    - README.md
  message: sample
"""
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("tul-package.yml", manifest)
        z.writestr("files/README.md", "sample\n")
        z.writestr("README.md", "sample package\n")


class PackageInboxIngestTest(unittest.TestCase):
    def test_external_download_package_is_moved_to_project_inbox_after_import(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            download = root / "Download"
            work = root / "termux" / "import" / "tul" / "work"
            download.mkdir(parents=True)
            work.mkdir(parents=True)
            source = download / "sample-package.zip"
            write_package(source)

            imported = import_package(source, {
                "platform": {
                    "inbox_roots": [str(download), str(work.parent / "inbox")],
                    "work_root": str(work),
                }
            })

            self.assertFalse(source.exists())
            self.assertTrue(imported.source.exists())
            self.assertIsNotNone(imported.ingested_source)
            self.assertTrue(Path(imported.ingested_source).exists())
            self.assertEqual(work.parent / "inbox", Path(imported.ingested_source).parent)

    def test_project_inbox_package_is_not_moved_again(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            work = root / "termux" / "import" / "tul" / "work"
            inbox = work.parent / "inbox"
            inbox.mkdir(parents=True)
            work.mkdir(parents=True, exist_ok=True)
            source = inbox / "sample-package.zip"
            write_package(source)

            imported = import_package(source, {
                "platform": {
                    "inbox_roots": [str(inbox)],
                    "work_root": str(work),
                }
            })

            self.assertTrue(source.exists())
            self.assertIsNone(imported.ingested_source)


if __name__ == "__main__":
    unittest.main()
