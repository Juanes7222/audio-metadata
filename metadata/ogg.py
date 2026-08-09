"""
OGG metadata writer.
"""

from __future__ import annotations

from pathlib import Path

from mutagen.oggvorbis import OggVorbis

from models import ParsedFile
from .base import BaseMetadataWriter


class OggMetadataWriter(BaseMetadataWriter):

    @property
    def supported_extensions(self) -> tuple[str, ...]:
        return (
            ".ogg",
        )

    def write(
        self,
        path: Path,
        parsed: ParsedFile,
    ) -> None:

        audio = OggVorbis(path)

        audio["tracknumber"] = f"{parsed.track:03d}"
        audio["title"] = parsed.title
        audio["artist"] = parsed.speaker_normalized
        audio["date"] = str(parsed.date.year)

        audio.save()