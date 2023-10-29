from __future__ import annotations

from watchdog.events import FileSystemEventHandler

from hanya.karma.config import KarmaConfigWatchDirectory

__all__ = (
    "BrushesIngestInotify",
    "BrushesIngestPolling",
)


class BrushesIngestInotify(FileSystemEventHandler):
    """
    A brushes to handle file ingestion.

    The following utilizes inotify system, where we can watch for FIEL_CLOSE_WRITE event.
    Useful for watching actual file changes.
    """

    def __init__(self, config: KarmaConfigWatchDirectory) -> None:
        self._config = config

    def on_closed(self, event):
        # TODO: Implement automatic ingest
        return super().on_closed(event)


class BrushesIngestPolling(FileSystemEventHandler):
    """
    A brushes to handle file ingestion.
    The following utilizes polling system.

    The internal use created/modified to determine whether to ingest or not.
    """

    def __init__(self, config: KarmaConfigWatchDirectory) -> None:
        self._config = config

    def on_created(self, event):
        return super().on_created(event)

    def on_modified(self, event):
        return super().on_modified(event)
