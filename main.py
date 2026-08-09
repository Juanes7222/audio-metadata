"""
Application entry point.
"""

from __future__ import annotations

import sys
from pathlib import Path

from bootstrap import build_processor
from cli import parse_args


def validate_directory(directory: Path) -> None:
    """
    Validates the input directory.
    """

    if not directory.exists():
        print(f"Directory does not exist: '{directory}'.")
        sys.exit(1)

    if not directory.is_dir():
        print(f"'{directory}' is not a directory.")
        sys.exit(1)


def main() -> None:
    """
    Application entry point.
    """

    args = parse_args()

    directory = Path(
        args.directory,
    ).expanduser().resolve()

    validate_directory(directory)

    processor = build_processor(
        args,
    )

    processor.process_directory(directory)


if __name__ == "__main__":
    main()