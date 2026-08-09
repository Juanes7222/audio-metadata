"""
Processing report.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections import defaultdict

from models import (
    FileDiagnosis,
    ProcessingResult,
)


class BaseReporter(ABC):
    """
    Base reporter interface.
    """

    @abstractmethod
    def report(
        self,
        results: list[ProcessingResult],
        diagnoses: list[FileDiagnosis],
        errors: list[tuple[str, str]],
    ) -> None:
        """
        Displays the processing report.
        """


class ConsoleReporter(BaseReporter):
    """
    Prints the processing report to the console.
    """

    _SEPARATOR = "=" * 80

    def report(
        self,
        results: list[ProcessingResult],
        diagnoses: list[FileDiagnosis],
        errors: list[tuple[str, str]],
    ) -> None:

        self._print_summary(
            results,
            diagnoses,
            errors,
        )

        if results:
            self._print_processed_files(results)

        if diagnoses:
            self._print_invalid_files(diagnoses)

        if errors:
            self._print_errors(errors)

    def _print_summary(
        self,
        results: list[ProcessingResult],
        diagnoses: list[FileDiagnosis],
        errors: list[tuple[str, str]],
    ) -> None:

        print()
        print(self._SEPARATOR)
        print("Processing completed")
        print(self._SEPARATOR)

        print(f"Processed files : {len(results)}")
        print(f"Invalid files   : {len(diagnoses)}")
        print(f"Errors          : {len(errors)}")
        print()

    def _print_processed_files(
        self,
        results: list[ProcessingResult],
    ) -> None:

        grouped: dict[str, list[ProcessingResult]] = defaultdict(list)

        for result in results:
            grouped[result.speaker_folder].append(result)

        print(self._SEPARATOR)
        print("Processed files")
        print(self._SEPARATOR)

        for speaker in sorted(grouped):

            print()
            print(f"[{speaker}]")

            for result in sorted(
                grouped[speaker],
                key=lambda item: item.track,
            ):

                print(
                    f"  {result.track:03d}  "
                    f"{result.final_name}"
                )

        print()

    def _print_invalid_files(
        self,
        diagnoses: list[FileDiagnosis],
    ) -> None:

        print(self._SEPARATOR)
        print("Invalid filenames")
        print(self._SEPARATOR)

        for diagnosis in diagnoses:

            print()
            print(diagnosis.filename)

            for issue in diagnosis.issues:
                print(f"  - {issue}")

        print()

    def _print_errors(
        self,
        errors: list[tuple[str, str]],
    ) -> None:

        print(self._SEPARATOR)
        print("Processing errors")
        print(self._SEPARATOR)

        for filename, message in errors:

            print()
            print(filename)
            print(f"  {message}")

        print()