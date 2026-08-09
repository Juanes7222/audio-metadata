"""
Command-line interface.
"""

from __future__ import annotations

from argparse import (
    ArgumentParser,
    BooleanOptionalAction,
    Namespace,
)


def create_parser() -> ArgumentParser:
    """
    Creates the command-line argument parser.
    """

    parser = ArgumentParser(
        prog="tag-audios",
        description=(
            "Rename audio files, organize them by speaker and update their metadata."
        ),
    )

    parser.add_argument(
        "--directory",
        required=True,
        metavar="PATH",
        help="Directory containing the audio files.",
    )

    parser.add_argument(
        "--create-folder",
        action=BooleanOptionalAction,
        default=True,
        help="Create one directory per speaker (default: enabled).",
    )
    
    parser.add_argument(
    "--track-strategy",
    choices=[
        "preserve",
        "generate",
        "reset",
    ],
    default="preserve",
    help=(
        "Track assignment strategy. "
        "'preserve' keeps existing tracks, "
        "'generate' creates tracks only for files without one, "
        "'reset' rebuilds the numbering from scratch."
    ),
)


    return parser


def parse_args() -> Namespace:
    """
    Parses the command-line arguments.
    """

    return create_parser().parse_args()