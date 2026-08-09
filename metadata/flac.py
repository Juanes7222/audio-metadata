"""
FLAC metadata writer.
"""

from __future__ import annotations

from pathlib import Path

from mutagen.flac import FLAC

from models import ParsedFile
from .base import BaseMetadataWriter


class FlacMetadataWriter(BaseMetadataWriter):

    @property
    def supported_extensions(self) -> tuple[str, ...]:
        return (".flac",)

    def write(
        self,
        path: Path,
        parsed: ParsedFile,
    ) -> None:

        audio = FLAC(path)

        audio["tracknumber"] = f"{parsed.track:03d}"
        audio["title"] = parsed.title
        audio["artist"] = parsed.speaker_display
        audio["date"] = str(parsed.date.year)

        audio.save()