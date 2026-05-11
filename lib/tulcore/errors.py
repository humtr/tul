"""Error types for tul."""
from __future__ import annotations


class TulError(Exception):
    """Base class for expected tul errors."""


class ConfigError(TulError):
    """Configuration could not be loaded, parsed, or validated."""


class GitError(TulError):
    """A git operation failed."""


class ManifestError(TulError):
    """A package manifest is missing or invalid."""


class PackageError(TulError):
    """A package could not be imported, inspected, or extracted safely."""


class SafetyError(TulError):
    """An operation was blocked by a safety guard."""


class CheckError(TulError):
    """A validation or check command failed."""
