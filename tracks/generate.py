"""
Track generation strategy.
"""

from __future__ import annotations

from .base import BaseTrackStrategy
from models import ParsedFile


class GenerateTrackStrategy(BaseTrackStrategy):
    """
    Preserves existing tracks and generates new ones for files
    without a track number.
    """

    def assign(
        self,
        files: list[ParsedFile],
        existing_tracks: set[int],
    ) -> None:

        used_tracks = set(existing_tracks)

        next_track = (
            max(used_tracks) + 1
            if used_tracks
            else 1
        )

        files.sort(
            key=lambda file: (
                file.original_track is None,
                file.original_track or 0,
                file.date,
            )
        )

        for file in files:

            if file.original_track is not None:

                if file.original_track in used_tracks:
                    raise ValueError(
                        f"Track {file.original_track:03d} already exists."
                    )

                file.assigned_track = file.original_track
                used_tracks.add(file.original_track)

                if file.original_track >= next_track:
                    next_track = file.original_track + 1

                continue

            file.assigned_track = next_track
            used_tracks.add(next_track)
            next_track += 1