from __future__ import annotations

from enum import Enum

from msgspec import Struct, field

__all__ = (
    "KarmaConfigMode",
    "KarmaConfigWatchDirectory",
    "KarmaConfigWatchOverride",
    "KarmaConfig",
)
DEFAULT_OUTPUT = r"{volume}.{chapter}"


def _default_priority() -> list[str]:
    return ["ROOT"]


class KarmaConfigMode(str, Enum):
    WATCH = "WATCH"
    POLLING = "POLLING"


class KarmaConfigWatchOverride(Struct):
    folder: str
    """:class:`str`: Folder name for the override."""
    output_format: str = field(default=DEFAULT_OUTPUT)


class KarmaConfigWatchDirectory(Struct):
    """Configuration for a directory to watch."""

    path: str
    """:class:`str`: Path to watch."""
    target: str
    """:class:`str`: The target folder or Komga library to sync to."""
    subdirectory: list[str] = field(default_factory=list)
    """:class:`list[str]`: Additional subdirectory that can be included."""
    priorities: list[str] = field(default_factory=_default_priority)
    """:class:`list[str]`: Priorities for the directory, `ROOT` is the highest priority by defaults."""
    publisher: str | None = field(default=None)
    """:class:`str | None`: Publisher that will be used when regex matching for split."""
    output_format: str = field(default=DEFAULT_OUTPUT)
    """:class:`str`: Output format for the directory."""
    overrides: list[KarmaConfigWatchOverride] = field(default_factory=list)
    """:class:`list[KarmaConfigWatchOverride]`: Overrides for specific folders."""


class KarmaConfig(Struct):
    """Configuration for Hanya."""

    mode: KarmaConfigMode = field(default=KarmaConfigMode.WATCH)
    """:class:`KarmaConfigMode`: Mode of operation for Hanya."""
    poll_interval: int = field(default=30, name="pollInterval")
    """:class:`int`: Interval in seconds to poll for changes."""
    watchdog: list[KarmaConfigWatchDirectory] = field(default_factory=list)
    """:class:`list[KarmaConfigWatchDirectory]`: List of directories to watch."""
