"""
Filename parser registry.
"""

from __future__ import annotations

from pathlib import Path

from models import (
    FileDiagnosis,
    ParseResult,
)
from .base import BaseFilenameParser
from .no_track import NoTrackFilenameParser
from .track import TrackFilenameParser


class ParserRegistry:
    """
    Registry containing all available filename parsers.
    """

    def __init__(
        self,
        parsers: list[BaseFilenameParser],
    ) -> None:

        self._parsers = parsers

    @classmethod
    def default(
        cls,
    ) -> "ParserRegistry":
        """
        Creates the default parser registry.
        """

        return cls(
            [
                TrackFilenameParser(),
                NoTrackFilenameParser(),
            ]
        )

    def parse(
        self,
        path: Path,
    ) -> ParseResult:

        for parser in self._parsers:

            parsed = parser.parse(path)

            if parsed is not None:
                return ParseResult(
                    parsed=parsed,
                    diagnosis=FileDiagnosis(
                        filename=path.name,
                    ),
                )

        return ParseResult(
            parsed=None,
            diagnosis=self._best_diagnosis(path),
        )

    def _best_diagnosis(
        self,
        path: Path,
    ) -> FileDiagnosis:

        return min(
            (
                parser.diagnose(path)
                for parser in self._parsers
            ),
            key=lambda item: len(item.issues),
        )