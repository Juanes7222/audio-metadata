"""
Filename diagnosis utilities.
"""

from __future__ import annotations

from dataclasses import dataclass

from models import FileDiagnosis
from validators import (
    validate_date,
    validate_speaker,
    validate_title,
    validate_track,
)


@dataclass(slots=True)
class FilenameDiagnosis:
    """
    Diagnoses invalid filenames.
    """

    require_track: bool

    def diagnose(
        self,
        filename: str,
    ) -> FileDiagnosis:

        diagnosis = FileDiagnosis(
            filename=filename,
        )

        parts = filename.split("_")

        expected = 4 if self.require_track else 3

        if len(parts) < expected:

            diagnosis.issues.append(
                f"Expected at least {expected} segments separated by '_', "
                f"but found {len(parts)}."
            )

            return diagnosis

        if self.require_track:
            self._diagnose_with_track(
                parts,
                diagnosis,
            )
        else:
            self._diagnose_without_track(
                parts,
                diagnosis,
            )

        if not diagnosis.issues:
            diagnosis.issues.append(
                "Filename does not match the expected pattern."
            )

        return diagnosis

    def _diagnose_with_track(
        self,
        parts: list[str],
        diagnosis: FileDiagnosis,
    ) -> None:

        self._append(
            validate_track(parts[0]),
            diagnosis,
        )

        self._append(
            validate_title(parts[1]),
            diagnosis,
        )

        self._append(
            validate_speaker(
                "_".join(parts[2:-1]),
            ),
            diagnosis,
        )

        self._append(
            validate_date(parts[-1]),
            diagnosis,
        )

    def _diagnose_without_track(
        self,
        parts: list[str],
        diagnosis: FileDiagnosis,
    ) -> None:

        self._append(
            validate_title(parts[0]),
            diagnosis,
        )

        self._append(
            validate_speaker(
                "_".join(parts[1:-1]),
            ),
            diagnosis,
        )

        self._append(
            validate_date(parts[-1]),
            diagnosis,
        )

    @staticmethod
    def _append(
        result,
        diagnosis: FileDiagnosis,
    ) -> None:

        if not result.valid:
            diagnosis.issues.append(
                result.message,
            )