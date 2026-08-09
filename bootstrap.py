"""
Application bootstrap.
"""

from __future__ import annotations

from argparse import Namespace

from metadata import MetadataRegistry
from parsers import ParserRegistry
from processor import AudioProcessor
from report import ConsoleReporter
from tracks import (
    TrackAllocator,
    TrackStrategyFactory,
)


def build_processor(
    args: Namespace,
) -> AudioProcessor:
    """
    Creates the application services.
    """

    return AudioProcessor(
        parser_registry=ParserRegistry.default(),
        metadata_registry=MetadataRegistry.default(),
        track_allocator=TrackAllocator(
            strategy=TrackStrategyFactory.create(
                args.track_strategy,
            ),
        ),
        reporter=ConsoleReporter(),
        create_folder=args.create_folder,
    )