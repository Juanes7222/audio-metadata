"""
Base classes for track assignment strategies.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from models import ParsedFile


class BaseTrackStrategy(ABC):
    """
    Base class for all track assignment strategies.
    """

    @abstractmethod
    def assign(
        self,
        files: list[ParsedFile],
        existing_tracks: set[int],
    ) -> None:
        """
        Assigns track numbers to the provided files.
        """