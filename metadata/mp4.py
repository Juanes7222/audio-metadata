"""
MP4/M4A metadata writer.
"""

from __future__ import annotations

from pathlib import Path

from mutagen.mp4 import MP4

from models import ParsedFile
from .base import BaseMetadataWriter


class Mp4MetadataWriter(BaseMetadataWriter):

    @property
    def supported_extensions(self) -> tuple[str, ...]:
        return (
            ".mp4",
            ".m4a",
        )

    def write(
        self,
        path: Path,
        parsed: ParsedFile,
    ) -> None:

        audio = MP4(path)

        audio["trkn"] = [(parsed.track, 0)]
        audio["\xa9nam"] = parsed.title
        audio["\xa9ART"] = parsed.speaker_display
        audio["\xa9day"] = str(parsed.date.year)
        audio["\xa9cmt"] = parsed.date.strftime("%d/%m/%Y")

        audio.save()