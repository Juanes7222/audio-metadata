"""
Filename parsers.
"""

from .base import BaseFilenameParser
from .no_track import NoTrackFilenameParser
from .registry import ParserRegistry
from .track import TrackFilenameParser

__all__ = [
    "BaseFilenameParser",
    "ParserRegistry",
    "TrackFilenameParser",
    "NoTrackFilenameParser",
]