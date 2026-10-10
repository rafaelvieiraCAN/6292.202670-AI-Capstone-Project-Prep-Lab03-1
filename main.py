"""Thin command-line entry point for the TVMaze summary package."""

from tvsummary import TVMazeSource, build_summary, write_summary
from tvsummary.config import OUTPUT_PATH


def main() -> int:
    """Fetch TVMaze records, summarize them, and write the report."""
    try:
        records = TVMazeSource().fetch_records()
        summary = build_summary(records)
        write_summary(summary, OUTPUT_PATH)
    except Exception as err:
        # Network and data failures should produce a useful message, not a traceback.
        print(f"Unable to create TVMaze summary: {err}")
        return 1

    print(f"Processed {len(records)} records.")
    print(f"Summary written to {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
