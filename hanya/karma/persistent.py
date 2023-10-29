from __future__ import annotations

from struct import Struct

from msgspec import field

__all__ = ("KarmaPersistency",)


class KarmaPersistency(Struct):
    path: str
    """:class:`str`: Path for the sync."""
    files: list[str] = field(default_factory=list)
    """:class:`list[str]`: List of files that are synced."""
