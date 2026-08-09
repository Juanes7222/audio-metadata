"""
Filename validators.
"""

from __future__ import annotations

from datetime import datetime

from models import ValidationResult


def validate_track(value: str) -> ValidationResult:

    if len(value) != 3:
        return ValidationResult(
            False,
            "Track number must contain exactly three digits.",
        )

    if not value.isdigit():
        return ValidationResult(
            False,
            "Track number must be numeric.",
        )

    return ValidationResult(True)


def validate_title(value: str) -> ValidationResult:

    if not value.strip():
        return ValidationResult(
            False,
            "Title cannot be empty.",
        )

    return ValidationResult(True)


def validate_speaker(value: str) -> ValidationResult:

    if not value.strip():
        return ValidationResult(
            False,
            "Speaker cannot be empty.",
        )

    return ValidationResult(True)


def validate_date(value: str) -> ValidationResult:

    try:
        datetime.strptime(
            value,
            "%d-%m-%Y",
        )
    except ValueError:
        return ValidationResult(
            False,
            "Date must use the format DD-MM-YYYY.",
        )

    return ValidationResult(True)