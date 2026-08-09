"""
Track reset strategy.
"""

from __future__ import annotations

from .base import BaseTrackStrategy
from models import ParsedFile


class ResetTrackStrategy(BaseTrackStrategy):
    """
    Ignores every existing track number and recreates the
    numbering from scratch using the recording date.
    """

    def assign(
        self,
        files: list[ParsedFile],
        existing_tracks: set[int],
    ) -> None:

        del existing_tracks

        files.sort(
            key=lambda file: (
                file.date,
                file.title.upper(),
            )
        )

        for index, file in enumerate(
            files,
            start=1,
        ):
            file.assigned_track = index