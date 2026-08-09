"""
Metadata writer registry.
"""

from __future__ import annotations

from pathlib import Path

from models import ParsedFile
from .base import BaseMetadataWriter
from .flac import FlacMetadataWriter
from .mp3 import Mp3MetadataWriter
from .mp4 import Mp4MetadataWriter
from .ogg import OggMetadataWriter


class MetadataRegistry:
    """
    Registry for metadata writers.
    """

    def __init__(
        self,
        writers: list[BaseMetadataWriter],
    ) -> None:

        self._writers: dict[str, BaseMetadataWriter] = {}

        for writer in writers:

            for extension in writer.supported_extensions:
                self._writers[
                    extension.lower()
                ] = writer

    @classmethod
    def default(
        cls,
    ) -> "MetadataRegistry":
        """
        Creates the default metadata registry.
        """

        return cls(
            [
                Mp3MetadataWriter(),
                FlacMetadataWriter(),
                OggMetadataWriter(),
                Mp4MetadataWriter(),
            ]
        )

    def write(
        self,
        path: Path,
        parsed: ParsedFile,
    ) -> None:
        """
        Writes metadata to an audio file.
        """

        extension = path.suffix.lower()

        writer = self._writers.get(extension)

        if writer is None:
            raise ValueError(
                f"No metadata writer registered for '{extension}'."
            )

        writer.write(
            path,
            parsed,
        )