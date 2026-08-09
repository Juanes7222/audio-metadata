"""
Audio processing orchestration.
"""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from metadata import MetadataRegistry
from models import (
    FileDiagnosis,
    ParsedFile,
    ProcessingResult,
)
from parsers import ParserRegistry
from report import BaseReporter
from tracks import TrackAllocator
from utils import is_audio_file


class AudioProcessor:
    """
    Coordinates the complete processing workflow.
    """

    def __init__(
        self,
        parser_registry: ParserRegistry,
        metadata_registry: MetadataRegistry,
        track_allocator: TrackAllocator,
        reporter: BaseReporter,
        create_folder: bool,
    ) -> None:
        self._parser_registry = parser_registry
        self._metadata_registry = metadata_registry
        self._track_allocator = track_allocator
        self._reporter = reporter
        self._create_folder = create_folder

    def process_directory(
        self,
        directory: Path,
    ) -> None:

        audio_files = self._collect_audio_files(directory)

        if not audio_files:
            print(
                f"No supported audio files were found in '{directory}'."
            )
            return

        parsed_files: list[ParsedFile] = []
        diagnoses: list[FileDiagnosis] = []
        results: list[ProcessingResult] = []
        errors: list[tuple[str, str]] = []

        for file in audio_files:

            result = self._parser_registry.parse(file)

            if result.parsed is None:
                diagnoses.append(result.diagnosis)
                continue

            parsed_files.append(result.parsed)

        groups = self._group_files(parsed_files)

        for speaker, files in groups.items():

            destination = self._prepare_destination(
                directory,
                speaker,
            )

            try:

                self._track_allocator.assign(
                    files=files,
                    directory=destination,
                )

            except Exception as exc:

                errors.append(
                    (
                        speaker,
                        str(exc),
                    )
                )

                continue

            files.sort(
                key=lambda item: item.track,
            )

            for parsed in files:

                destination_file = (
                    destination /
                    self._build_filename(parsed)
                )

                try:

                    parsed.path.rename(
                        destination_file,
                    )

                    self._metadata_registry.write(
                        destination_file,
                        parsed,
                    )

                    results.append(
                        ProcessingResult(
                            original_name=parsed.path.name,
                            final_name=destination_file.name,
                            speaker_folder=speaker,
                            track=parsed.track,
                        )
                    )

                except Exception as exc:

                    errors.append(
                        (
                            parsed.path.name,
                            str(exc),
                        )
                    )

        self._reporter.report(
            results=results,
            diagnoses=diagnoses,
            errors=errors,
        )

    @staticmethod
    def _collect_audio_files(
        directory: Path,
    ) -> list[Path]:

        return sorted(
            file
            for file in directory.iterdir()
            if is_audio_file(file)
        )

    def _group_files(
        self,
        parsed_files: list[ParsedFile],
    ) -> dict[str, list[ParsedFile]]:

        if not self._create_folder:
            return {
                "": parsed_files,
            }

        grouped: dict[
            str,
            list[ParsedFile],
        ] = defaultdict(list)

        for parsed in parsed_files:

            grouped[
                parsed.speaker_raw
            ].append(parsed)

        return grouped
    
    def _prepare_destination(
        self,
        root: Path,
        speaker: str,
    ) -> Path:
        """
        Returns the destination directory.
        """

        if not self._create_folder:
            return root

        destination = root / speaker

        destination.mkdir(
            parents=True,
            exist_ok=True,
        )

        return destination

    @staticmethod
    def _collect_existing_tracks(
        directory: Path,
    ) -> set[int]:
        """
        Collects every existing track number inside the destination
        directory.
        """

        tracks: set[int] = set()

        if not directory.exists():
            return tracks

        for file in directory.iterdir():

            if not is_audio_file(file):
                continue

            stem = file.stem

            if len(stem) < 3:
                continue

            prefix = stem[:3]

            if not prefix.isdigit():
                continue

            tracks.add(int(prefix))

        return tracks

    @staticmethod
    def _build_filename(
        parsed: ParsedFile,
    ) -> str:
        """
        Builds the destination filename.
        """

        title = " ".join(
            parsed.title.upper().split()
        )

        date = parsed.date.strftime(
            "%d-%m-%Y"
        )

        return (
            f"{parsed.track:03d}_"
            f"{title}_"
            f"{parsed.speaker_raw}_"
            f"{date}"
            f"{parsed.path.suffix.lower()}"
        )