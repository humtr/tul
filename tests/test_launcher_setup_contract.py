from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path

from helpers import REPO_ROOT, read_text

sys.path.insert(0, str(REPO_ROOT / "lib"))

from tulcore.launcher import PATH_PROFILE_LINE, install_launcher  # noqa: E402


class LauncherSetupContractTest(unittest.TestCase):
    def test_install_scripts_use_canonical_setup_install(self) -> None:
        termux = read_text("scripts/install-termux.sh")
        windows = read_text("scripts/install-windows.ps1")
        self.assertIn("setup install", termux)
        self.assertIn("setup install", windows)
        self.assertNotIn(' bin/tul" install', termux)
        self.assertNotIn("$Tul install", windows)

    @unittest.skipIf(os.name == "nt", "POSIX launcher profile behavior is not used on Windows")
    def test_posix_setup_install_creates_launcher_and_profile_hint(self) -> None:
        old_home = os.environ.get("HOME")
        try:
            with tempfile.TemporaryDirectory() as tmp:
                os.environ["HOME"] = tmp
                output = install_launcher(REPO_ROOT, force=True)
                launcher = Path(tmp) / "bin" / "tul"
                profile = Path(tmp) / ".profile"
                self.assertTrue(launcher.exists() or launcher.is_symlink())
                self.assertIn(PATH_PROFILE_LINE, profile.read_text(encoding="utf-8"))
                self.assertIn("# tul setup install", output)
                self.assertIn("launcher:", output)
        finally:
            if old_home is None:
                os.environ.pop("HOME", None)
            else:
                os.environ["HOME"] = old_home


if __name__ == "__main__":
    unittest.main()
