"""Data model for one TVMaze television show."""

from typing import Any


class ShowRecord:
    """Represent one show and normalize missing or malformed source values."""

    def __init__(self, data: dict[str, Any]):
        """Create a record from a TVMaze API dictionary."""
        data = data if isinstance(data, dict) else {}
        self.name = self._clean_text(data.get("name"))
        self.language = self._clean_text(data.get("language"))
        self.genres = self._clean_genres(data.get("genres"))
        self.premiered = self._clean_text(data.get("premiered"))
        self.rating = self._clean_rating(data.get("rating"))
        self.network = self._clean_network(data.get("network"))

    @staticmethod
    def _clean_text(value: Any) -> str | None:
        if not isinstance(value, str) or not value.strip():
            return None
        return value.strip()

    @staticmethod
    def _clean_genres(value: Any) -> list[str]:
        if not isinstance(value, list):
            return []
        return [item.strip() for item in value if isinstance(item, str) and item.strip()]

    @staticmethod
    def _clean_rating(value: Any) -> float | None:
        if not isinstance(value, dict):
            return None
        rating = value.get("average")
        if isinstance(rating, bool) or not isinstance(rating, (int, float)):
            return None
        return float(rating)

    @staticmethod
    def _clean_network(value: Any) -> str | None:
        if not isinstance(value, dict):
            return None
        name = value.get("name")
        if not isinstance(name, str) or not name.strip():
            return None
        return name.strip()

    def __str__(self) -> str:
        """Return a readable short description of the show."""
        return self.name or "Unknown show"
