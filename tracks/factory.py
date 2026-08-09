"""
Factory for track assignment strategies.
"""

from __future__ import annotations

from .base import BaseTrackStrategy
from .generate import GenerateTrackStrategy
from .preserve import PreserveTrackStrategy
from .reset import ResetTrackStrategy


class TrackStrategyFactory:
    """
    Creates track assignment strategies.
    """

    _STRATEGIES: dict[str, type[BaseTrackStrategy]] = {
        "preserve": PreserveTrackStrategy,
        "generate": GenerateTrackStrategy,
        "reset": ResetTrackStrategy,
    }

    @classmethod
    def create(
        cls,
        strategy: str,
    ) -> BaseTrackStrategy:

        try:
            return cls._STRATEGIES[strategy.lower()]()
        except KeyError as exc:
            available = ", ".join(sorted(cls._STRATEGIES))

            raise ValueError(
                f"Unknown track strategy '{strategy}'. "
                f"Available strategies: {available}."
            ) from exc