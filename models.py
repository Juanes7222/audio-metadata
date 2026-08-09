"""
Application models.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path


@dataclass(slots=True)
class ParsedFile:
    """
    Represents a successfully parsed audio file.
    """

    path: Path
    title: str
    speaker_raw: str
    speaker_normalized: str
    date: datetime
    original_track: int | None = None
    assigned_track: int | None = None

    @property
    def track(self) -> int:
        """
        Returns the final track number.
        """

        if self.assigned_track is None:
            raise RuntimeError(
                "Track number has not been assigned."
            )

        return self.assigned_track
    
    @property
    def speaker_display(self) -> str:
        """
        Returns the speaker name formatted for display.
        """
        return self.speaker_raw.title()


@dataclass(slots=True)
class FileDiagnosis:
    """
    Represents the diagnosis of an invalid filename.
    """

    filename: str
    issues: list[str] = field(default_factory=list)

    @property
    def valid(self) -> bool:
        return not self.issues


@dataclass(slots=True)
class ProcessingResult:
    """
    Represents a successfully processed file.
    """

    original_name: str
    final_name: str
    speaker_folder: str
    track: int


@dataclass(slots=True)
class ValidationResult:
    """
    Result returned by a validator.
    """

    valid: bool
    message: str = ""

@dataclass(slots=True)
class ParseResult:
    """
    Result returned by the parser registry.
    """

    parsed: ParsedFile | None
    diagnosis: FileDiagnosis