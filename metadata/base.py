"""
Base class for metadata writers.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from models import ParsedFile


class BaseMetadataWriter(ABC):
    """
    Base class for metadata writers.
    """

    @property
    @abstractmethod
    def supported_extensions(self) -> tuple[str, ...]:
        """
        File extensions supported by this writer.
        """

    @abstractmethod
    def write(
        self,
        path: Path,
        parsed: ParsedFile,
    ) -> None:
        """
        Writes metadata to the audio file.
        """