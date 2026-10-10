# TVMaze Show Summary

This package downloads television show records from the TVMaze API and summarizes genres, ratings by language, premiere decades, and unique networks.

## Data source

- URL: https://api.tvmaze.com/shows?page=0
- One record represents one television show.
- The Lab 02 solution describes approximately 250 records from this endpoint.

## Setup

```bash
conda env create -f environment.yml
conda activate tvsummary
pip install -r requirements.txt
pip install -e .
```

## Run

```bash
python main.py
```

The report is written to `data/processed/summary.json`.

## Test

```bash
python -m unittest discover -s tests
```

The tests use handmade records and do not make network requests.

## Layout

- `main.py`: thin entry point; connects fetching, summarizing, writing, and user-facing error handling.
- `src/tvsummary/__init__.py`: re-exports the package's public classes and functions.
- `config.py`: central source URL, timeout, and output path.
- `models.py`: `ShowRecord`, which cleans fields when each record is created.
- `sources.py`: `TVMazeSource`, the only module that imports `requests`.
- `aggregations.py`: `Aggregation` base class and concrete aggregation subclasses.
- `report.py`: combines aggregation results and writes JSON.
- `tests/test_models.py`: offline unit tests for record cleanup and aggregation behavior.
- `data/processed/summary.json`: committed example output from the supplied Lab 02 files.

## What moved where

| Lab 02 function or constant | Lab 03 location |
|---|---|
| `SOURCE_URL` | `tvsummary.config.SOURCE_URL` |
| `fetch_records(url)` | `TVMazeSource.fetch_records()` in `sources.py` |
| Raw show dictionaries and field checks | `ShowRecord.__init__()` and cleaning helpers in `models.py` |
| `shows_per_genre(records)` | `ShowsPerGenre.compute()` in `aggregations.py` |
| `average_rating_by_language(records)` | `AverageRatingByLanguage.compute()` in `aggregations.py` |
| `shows_per_decade(records)` | `ShowsPerDecade.compute()` in `aggregations.py` |
| `unique_networks(records)` | `UniqueNetworks.compute()` in `aggregations.py` |
| `build_summary(records)` | `build_summary(records)` in `report.py` |
| `write_summary(summary, path)` | `write_summary(summary, path)` in `report.py` |
| `main()` | `main()` in root `main.py` |

## Design choices

`ShowRecord` represents one show and normalizes missing or malformed fields at construction time, so aggregation classes do not need to repeat defensive checks. `TVMazeSource` owns the HTTP request and returns model objects instead of raw dictionaries.

`Aggregation` defines the common `compute()` interface. `ShowsPerGenre`, `AverageRatingByLanguage`, `ShowsPerDecade`, and `UniqueNetworks` override that method with their own calculations. `build_summary()` loops over aggregation objects and calls `compute()` without checking each subclass's type. To add another statistic, create a subclass, implement `compute()`, set its output `key`, and add it to the list in `build_summary()`.

The source URL, request timeout, and report path are kept together in `config.py`. The report writer creates the output directory when needed. Only `sources.py` imports `requests`.

## Known limitations

The example `summary.json` is carried forward from the supplied Lab 02 files; live data may change when the API is queried again. The current implementation treats malformed ratings as missing and ignores malformed premiere years. It requires an internet connection for a normal run, but offline tests do not require one.
