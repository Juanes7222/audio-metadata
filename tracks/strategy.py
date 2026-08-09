"""
Track assignment strategies.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from models import ParsedFile


class TrackAssignmentStrategy(ABC):

    @abstractmethod
    def assign(
        self,
        files: list[ParsedFile],
        existing_tracks: set[int],
        generate_missing: bool,
    ) -> None:
        ...


class SequentialTrackStrategy(TrackAssignmentStrategy):

    def assign(
        self,
        files: list[ParsedFile],
        existing_tracks: set[int],
        generate_missing: bool,
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

            if not generate_missing:
                raise ValueError(
                    f"'{file.path.name}' does not contain a track number."
                )

            file.assigned_track = next_track
            used_tracks.add(next_track)
            next_track += 1