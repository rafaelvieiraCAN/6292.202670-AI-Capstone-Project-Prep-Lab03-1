"""Polymorphic aggregation classes for TVMaze show records."""

from abc import ABC, abstractmethod
from collections import Counter

from .models import ShowRecord


class Aggregation(ABC):
    """Base class for a summary statistic computed from show records."""

    key = ""

    def __init__(self, records: list[ShowRecord]):
        """Store the records to be summarized."""
        self.records = records

    @abstractmethod
    def compute(self):
        """Return this aggregation's result."""
        raise NotImplementedError


class ShowsPerGenre(Aggregation):
    """Count records per genre, ordered by descending count."""

    key = "shows_per_genre"

    def compute(self) -> dict[str, int]:
        counts = Counter(genre for record in self.records for genre in record.genres)
        return dict(sorted(counts.items(), key=lambda item: item[1], reverse=True))


class AverageRatingByLanguage(Aggregation):
    """Calculate mean rating by language, excluding missing values."""

    key = "average_rating_by_language"

    def compute(self) -> dict[str, float]:
        totals: dict[str, float] = {}
        counts: dict[str, int] = {}
        for record in self.records:
            if record.language is None or record.rating is None:
                continue
            totals[record.language] = totals.get(record.language, 0.0) + record.rating
            counts[record.language] = counts.get(record.language, 0) + 1
        averages = {
            language: round(totals[language] / counts[language], 2)
            for language in totals
        }
        return dict(sorted(averages.items(), key=lambda item: item[1], reverse=True))


class ShowsPerDecade(Aggregation):
    """Count shows by premiere decade in ascending decade order."""

    key = "shows_per_decade"

    def compute(self) -> dict[str, int]:
        counts: Counter[str] = Counter()
        for record in self.records:
            if not record.premiered:
                continue
            try:
                year = int(record.premiered[:4])
            except (ValueError, TypeError):
                continue
            decade = f"{(year // 10) * 10}s"
            counts[decade] += 1
        return dict(sorted(counts.items()))


class UniqueNetworks(Aggregation):
    """Count distinct non-empty network names."""

    key = "unique_networks"

    def compute(self) -> int:
        return len({record.network for record in self.records if record.network})
