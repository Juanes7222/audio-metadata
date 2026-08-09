"""
Parser for filenames containing track numbers.
"""

from __future__ import annotations

import re

from .base import BaseFilenameParser


class TrackFilenameParser(BaseFilenameParser):
    """
    Parses filenames with the following format:

        001_TITLE_SPEAKER_DD-MM-YYYY
    """

    has_track = True

    pattern = re.compile(
        r"""
        ^
        (?P<track>\d{3})
        _
        (?P<title>.+?)
        _
        (?P<speaker>.+?)
        _
        (?P<date>\d{2}-\d{2}-\d{4})
        $
        """,
        re.VERBOSE,
    )