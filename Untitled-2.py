"""
AIGC 5005 - Lab 02
TVMaze Show Aggregator

Downloads TV show records and creates summary statistics.
"""

from pathlib import Path
import json
import requests

SOURCE_URL = "https://api.tvmaze.com/shows?page=0"


def fetch_records(url):
    """
    Download the records and return them as Python objects.
    """

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()

    except requests.RequestException as err:
        print(f"Download failed: {err}")
        raise SystemExit(1)


def shows_per_genre(records):
    """
    Count the number of shows in each genre.
    """

    genre_counts = {}

    for show in records:
        genres = show.get("genres", [])

        for genre in genres:
            genre_counts[genre] = genre_counts.get(genre, 0) + 1

    return dict(sorted(
        genre_counts.items(),
        key=lambda item: item[1],
        reverse=True
    ))


def average_rating_by_language(records):
    """
    Calculate average show rating by language.
    """

    language_totals = {}
    language_counts = {}

    for show in records:

        language = show.get("language")

        rating_info = show.get("rating", {})
        rating = rating_info.get("average")

        if language is None:
            continue

        if rating is None:
            continue

        language_totals[language] = (
            language_totals.get(language, 0) + rating
        )

        language_counts[language] = (
            language_counts.get(language, 0) + 1
        )

    averages = {}

    for language in language_totals:

        averages[language] = round(
            language_totals[language] /
            language_counts[language],
            2
        )

    return dict(sorted(
        averages.items(),
        key=lambda item: item[1],
        reverse=True
    ))


def shows_per_decade(records):
    """
    Count shows premiered by decade.
    """

    decade_counts = {}

    for show in records:

        premiered = show.get("premiered")

        if not premiered:
            continue

        try:
            year = int(premiered[:4])
            decade = f"{(year // 10) * 10}s"

            decade_counts[decade] = (
                decade_counts.get(decade, 0) + 1
            )

        except (ValueError, TypeError):
            continue

    return dict(sorted(decade_counts.items()))


def unique_networks(records):
    """
    Demonstrates use of a set collection.
    """

    networks = {
        show["network"]["name"]
        for show in records
        if show.get("network")
        and show["network"].get("name")
    }

    return len(networks)


def build_summary(records):
    """
    Combine the aggregations into one dictionary.
    """

    summary = {
        "source_url": SOURCE_URL,
        "records_processed": len(records),
        "unique_networks": unique_networks(records),
        "shows_per_genre": shows_per_genre(records),
        "average_rating_by_language":
            average_rating_by_language(records),
        "shows_per_decade": shows_per_decade(records)
    }

    return summary


def write_summary(summary, path):
    """
    Write summary data to a JSON file.
    """

    output_path = Path(path)

    with output_path.open(
        "w",
        encoding="utf-8"
    ) as outfile:

        json.dump(
            summary,
            outfile,
            indent=2,
            ensure_ascii=False
        )


def main():

    records = fetch_records(SOURCE_URL)

    summary = build_summary(records)

    write_summary(summary, "summary.json")

    print(
        f"Processed {len(records)} records."
    )
    print("Summary written to summary.json")


if __name__ == "__main__":
    main()