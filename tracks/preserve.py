"""
Track preservation strategy.
"""

from __future__ import annotations

from .base import BaseTrackStrategy
from models import ParsedFile


class PreserveTrackStrategy(BaseTrackStrategy):
    """
    Preserves every existing track number.

    Every file must already contain a valid track number.
    """

    def assign(
        self,
        files: list[ParsedFile],
        existing_tracks: set[int],
    ) -> None:

        used_tracks = set(existing_tracks)

        files.sort(
            key=lambda file: (
                file.original_track or 0,
                file.date,
            )
        )

        for file in files:

            if file.original_track is None:
                raise ValueError(
                    f"'{file.path.name}' does not contain a track number."
                )

            if file.original_track in used_tracks:
                raise ValueError(
                    f"Track {file.original_track:03d} already exists."
                )

            file.assigned_track = file.original_track
            used_tracks.add(file.original_track)