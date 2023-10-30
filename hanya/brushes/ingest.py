from __future__ import annotations

from pathlib import Path

from nmanga import exporter, file_handler
from nmanga.common import RegexCollection, check_cbz_exist, create_chapter
from nmanga.utils import secure_filename, unsecure_filename
from watchdog.events import FileClosedEvent, FileSystemEventHandler, LoggingEventHandler

from hanya.karma.config import KarmaConfigWatchDirectory
from hanya.tooling import get_logger

__all__ = (
    "BrushesIngestInotify",
    "BrushesIngestPolling",
)


class _BrushesIngestBase(FileSystemEventHandler):
    def __init__(self, config: KarmaConfigWatchDirectory, *, name: str) -> None:
        logger = get_logger(f"hanya.brushes.ingest.{name}")
        logging = LoggingEventHandler(logger=logger)
        self.logger = logger
        self._logger = logging
        self._config = config

    def on_any_event(self, event):
        self._logger.on_any_event(event)
        return super().on_any_event(event)

    def dispatch(self, event):
        self._logger.dispatch(event)
        return super().dispatch(event)


class BrushesIngestInotify(_BrushesIngestBase):
    """
    A brushes to handle file ingestion.

    The following utilizes inotify system, where we can watch for FIEL_CLOSE_WRITE event.
    Useful for watching actual file changes.
    """

    def __init__(self, config: KarmaConfigWatchDirectory) -> None:
        super().__init__(config, name="inotify")

    def dispatch(self, event):
        return super().dispatch(event)

    def on_closed(self, event: FileClosedEvent) -> None:
        if event.is_directory:
            self.logger.debug(f"Event is directory: {event.src_path}, skipping!")
            return
        src_path = Path(event.src_path)
        self.logger.info(f"File closed: {src_path}, trying to ingest...")
        parent = src_path.parent
        if parent.stem in self._config.subdirectory:
            self.logger.debug(f"Parent is subdirectory: {parent}, going up once more for title")
            parent = parent.parent

        chapter_re = RegexCollection.chapter_re(parent.stem)
        if self._config.publisher:
            chapter_re = RegexCollection.chapter_re(parent.stem, self._config.publisher)

        target_dir = Path(self._config.target) / parent.stem
        target_dir.mkdir(parents=True, exist_ok=True)

        collected_chapters = {}
        skipped_chapters: list[str] = []
        try:
            with file_handler.MangaArchive(src_path) as archive:
                for image, _ in archive:
                    filename = image.filename
                    match_re = chapter_re.match(Path(filename).name)
                    if not match_re:
                        self.logger.error(f"Unable to match chapter: {filename}")
                        self.logger.error("Exiting...")
                        return
                    chapter_data = create_chapter(match_re, self._config.publisher is not None)
                    if chapter_data in skipped_chapters:
                        continue

                    if chapter_data not in collected_chapters:
                        target_archive = unsecure_filename(secure_filename(chapter_data))
                        if check_cbz_exist(target_dir, target_archive):
                            self.logger.warning(f"Skipping chapter: {chapter_data}, already exists!")
                            skipped_chapters.append(chapter_data)
                            continue
                        self.logger.info(f"Creating chapter: {chapter_data}")
                        collected_chapters[chapter_data] = exporter.CBZMangaExporter(target_archive, target_dir)

                    image_bita = archive.read(image)
                    collected_chapters[chapter_data].add_image(Path(filename).name, image_bita)
        except NotImplementedError:
            self.logger.error("Unable to handle non-archive files!")
            return

        for chapter, cbz_export in collected_chapters.items():
            self.logger.info(f"Finishing chapter: {chapter}")
            cbz_export.close()

        self.logger.info(f"Finished ingesting: {src_path}")


class BrushesIngestPolling(_BrushesIngestBase):
    """
    A brushes to handle file ingestion.
    The following utilizes polling system.

    The internal use created/modified to determine whether to ingest or not.
    """

    def __init__(self, config: KarmaConfigWatchDirectory) -> None:
        super().__init__(config, name="polling")

    def on_created(self, event):
        return super().on_created(event)

    def on_modified(self, event):
        return super().on_modified(event)
