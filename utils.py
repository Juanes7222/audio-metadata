"""
General utility functions.
"""

from __future__ import annotations

import re
import unicodedata
from pathlib import Path


SUPPORTED_EXTENSIONS = {
    ".mp3",
    ".flac",
    ".ogg",
    ".m4a",
    ".mp4",
}


def is_audio_file(path: Path) -> bool:
    """
    Returns whether the file is a supported audio format.
    """

    return path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS


def normalize_name(value: str) -> str:
    """
    Normalizes names for comparisons.
    """

    normalized = unicodedata.normalize(
        "NFKD",
        value,
    )

    normalized = normalized.encode(
        "ascii",
        "ignore",
    ).decode()

    normalized = normalized.upper()

    normalized = re.sub(
        r"\s+",
        " ",
        normalized,
    )

    return normalized.strip()


def collapse_spaces(value: str) -> str:
    """
    Removes duplicated spaces.
    """

    return " ".join(value.split())