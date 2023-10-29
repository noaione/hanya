from __future__ import annotations

import threading
from typing import TypedDict

from hanya.karma.config import KarmaConfig
from hanya.watcher import HanyaWatchdog

__all__ = ("Hanya",)


class _ThreadsData(TypedDict):
    thread: threading.Thread
    watcher: HanyaWatchdog


class Hanya:
    _threads: dict[str, _ThreadsData]

    def __init__(self, config: KarmaConfig) -> None:
        self._config = config

    def start(self):
        # Assign each watcher to a thread
        threads: dict[str, _ThreadsData] = {}
        for config in self._config.watchdog:
            watcher = HanyaWatchdog(config, self._config)
            t = threading.Thread(target=watcher.start)
            # Assign stop method to thread
            t.start()
            threads[config.path] = {
                "thread": t,
                "watcher": watcher,
            }

        self._threads = threads

    def stop(self, timeout: float | None = None):
        for _, data in self._threads.items():
            data["watcher"].stop(timeout)
            data["thread"].join(timeout)
