"""Public interface for the TVMaze summary package."""

from .aggregations import (
    Aggregation,
    AverageRatingByLanguage,
    ShowsPerDecade,
    ShowsPerGenre,
    UniqueNetworks,
)
from .models import ShowRecord
from .report import build_summary, write_summary
from .sources import TVMazeSource

__all__ = [
    "Aggregation",
    "AverageRatingByLanguage",
    "ShowsPerDecade",
    "ShowRecord",
    "ShowsPerGenre",
    "TVMazeSource",
    "UniqueNetworks",
    "build_summary",
    "write_summary",
]
