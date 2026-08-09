"""
Parser for filenames without track numbers.
"""

from __future__ import annotations

import re

from .base import BaseFilenameParser


class NoTrackFilenameParser(BaseFilenameParser):
    """
    Parses filenames with the following format:

        TITLE_SPEAKER_DD-MM-YYYY
    """

    has_track = False

    pattern = re.compile(
        r"""
        ^
        (?P<title>.+?)
        _
        (?P<speaker>.+?)
        _
        (?P<date>\d{2}-\d{2}-\d{4})
        $
        """,
        re.VERBOSE,
    )