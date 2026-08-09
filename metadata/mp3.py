"""
MP3 metadata writer.
"""

from __future__ import annotations

from pathlib import Path

from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3

from models import ParsedFile
from .base import BaseMetadataWriter


class Mp3MetadataWriter(BaseMetadataWriter):

    @property
    def supported_extensions(self) -> tuple[str, ...]:
        return (".mp3",)

    def write(
        self,
        path: Path,
        parsed: ParsedFile,
    ) -> None:

        audio = MP3(path, ID3=EasyID3)

        audio["tracknumber"] = f"{parsed.track:03d}"
        audio["title"] = parsed.title
        audio["artist"] = parsed.speaker_display
        audio["date"] = str(parsed.date.year)

        audio.save()