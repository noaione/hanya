from __future__ import annotations

from watchdog.observers import Observer
from watchdog.observers.api import BaseObserver
from watchdog.observers.polling import PollingObserver

from hanya.brushes import BrushesIngestInotify
from hanya.brushes.ingest import BrushesIngestPolling
from hanya.karma.config import KarmaConfig, KarmaConfigWatchDirectory

__all__ = ("HanyaWatchdog",)


class HanyaWatchdog:
    _handler: BrushesIngestInotify | BrushesIngestPolling
    _observer: BaseObserver

    def __init__(self, config: KarmaConfigWatchDirectory, parent_config: KarmaConfig, /) -> None:
        self._config = config
        self._parent_config = parent_config
        self._init()

    def _init(self):
        observer = Observer()
        if isinstance(observer, PollingObserver):
            self._handler = BrushesIngestPolling(self._config)
        else:
            cls_name = type(observer).__name__
            # Check if Inotify is available
            if cls_name.startswith("Inotify"):
                self._handler = BrushesIngestInotify(self._config)
            else:
                self._handler = BrushesIngestPolling(self._config)
        observer.schedule(self._handler, self._config.path, recursive=True)
        self._observer = observer

    def start(self) -> None:
        self._observer.start()

    def stop(self, timeout: float | None = None, /):
        self._observer.stop()
        self._observer.join(timeout)
