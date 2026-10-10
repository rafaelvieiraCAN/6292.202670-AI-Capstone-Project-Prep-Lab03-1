"""Build the summary dictionary and write it as JSON."""

import json
from pathlib import Path
from typing import Iterable

from .aggregations import (
    Aggregation,
    AverageRatingByLanguage,
    ShowsPerDecade,
    ShowsPerGenre,
    UniqueNetworks,
)
from .config import SOURCE_URL
from .models import ShowRecord


def build_summary(records: Iterable[ShowRecord]) -> dict:
    """Build a summary with the same keys and calculations as Lab 02."""
    records = list(records)
    aggregations: list[Aggregation] = [
        UniqueNetworks(records),
        ShowsPerGenre(records),
        AverageRatingByLanguage(records),
        ShowsPerDecade(records),
    ]
    summary = {
        "source_url": SOURCE_URL,
        "records_processed": len(records),
    }
    # Polymorphism: each aggregation supplies its own implementation of compute().
    for aggregation in aggregations:
        summary[aggregation.key] = aggregation.compute()
    return summary


def write_summary(summary: dict, path: str | Path) -> None:
    """Write the summary as UTF-8 JSON, creating parent folders if needed."""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as outfile:
        json.dump(summary, outfile, indent=2, ensure_ascii=False)
        outfile.write("\n")
