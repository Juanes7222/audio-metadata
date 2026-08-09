"""
Base classes for filename parsers.
"""

from __future__ import annotations

from abc import ABC
from datetime import datetime
from pathlib import Path
from re import Match, Pattern

from models import ParsedFile
from utils import collapse_spaces, normalize_name
from .diagnosis import FilenameDiagnosis


class BaseFilenameParser(ABC):
    """
    Base implementation shared by all filename parsers.
    """

    pattern: Pattern[str]
    has_track: bool

    def __init__(self) -> None:
        self._diagnosis = FilenameDiagnosis(
            require_track=self.has_track,
        )

    def parse(
        self,
        path: Path,
    ) -> ParsedFile | None:

        match = self.pattern.fullmatch(path.stem)

        if match is None:
            return None

        try:
            date = datetime.strptime(
                match.group("date"),
                "%d-%m-%Y",
            )
        except ValueError:
            return None

        speaker = collapse_spaces(
            match.group("speaker"),
        )

        title = collapse_spaces(
            match.group("title"),
        )

        return ParsedFile(
            path=path,
            title=title,
            speaker_raw=speaker,
            speaker_normalized=normalize_name(
                speaker,
            ),
            date=date,
            original_track=self._extract_track(match),
        )

    def diagnose(self, path: Path):
        return self._diagnosis.diagnose(path.stem)

    def _extract_track(
        self,
        match: Match[str],
    ) -> int | None:

        if not self.has_track:
            return None

        return int(match.group("track"))