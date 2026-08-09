"""
Track allocation service.
"""

from __future__ import annotations

from pathlib import Path

from models import ParsedFile
from utils import is_audio_file
from .base import BaseTrackStrategy


class TrackAllocator:
    """
    Coordinates track assignment.
    """

    def __init__(
        self,
        strategy: BaseTrackStrategy,
    ) -> None:
        self._strategy = strategy

    def assign(
        self,
        files: list[ParsedFile],
        directory: Path,
    ) -> None:
        """
        Assigns track numbers using the configured strategy.
        """

        existing_tracks = self._collect_existing_tracks(
            directory,
            files,
        )

        self._strategy.assign(
            files,
            existing_tracks,
        )

    @staticmethod
    def _collect_existing_tracks(
        directory: Path,
        processing_files: list[ParsedFile],
    ) -> set[int]:
        """
        Collects track numbers already present in the destination
        directory, excluding the files currently being processed.
        """

        ignored = {
            file.path.resolve()
            for file in processing_files
        }

        tracks: set[int] = set()

        if not directory.exists():
            return tracks

        for file in directory.iterdir():

            if file.resolve() in ignored:
                continue

            if not is_audio_file(file):
                continue

            stem = file.stem

            if len(stem) < 3:
                continue

            prefix = stem[:3]

            if prefix.isdigit():
                tracks.add(int(prefix))

        return tracks