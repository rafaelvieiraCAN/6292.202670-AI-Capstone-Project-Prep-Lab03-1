"""Offline tests for TVMaze record cleaning and aggregation behavior."""

import unittest

from tvsummary import ShowRecord, ShowsPerGenre, ShowsPerDecade


class ShowRecordTests(unittest.TestCase):
    def test_cleans_missing_and_malformed_values(self):
        record = ShowRecord({
            "name": "  Example Show  ",
            "language": None,
            "genres": ["Drama", "", 42, "Comedy"],
            "premiered": "not-a-date",
            "rating": {"average": "not numeric"},
            "network": {"name": "  Network One  "},
        })
        self.assertEqual(record.name, "Example Show")
        self.assertIsNone(record.language)
        self.assertEqual(record.genres, ["Drama", "Comedy"])
        self.assertIsNone(record.rating)
        self.assertEqual(record.network, "Network One")
        self.assertEqual(str(record), "Example Show")

    def test_missing_record_fields_are_safe(self):
        record = ShowRecord({})
        self.assertEqual(str(record), "Unknown show")
        self.assertEqual(record.genres, [])
        self.assertIsNone(record.rating)
        self.assertIsNone(record.network)

    def test_aggregations_use_handmade_records(self):
        records = [
            ShowRecord({"genres": ["Drama"], "premiered": "1994-01-01"}),
            ShowRecord({"genres": ["Drama", "Comedy"], "premiered": "2002-05-01"}),
            ShowRecord({"genres": ["Comedy"], "premiered": "invalid"}),
        ]
        self.assertEqual(ShowsPerGenre(records).compute(), {"Drama": 2, "Comedy": 2})
        self.assertEqual(ShowsPerDecade(records).compute(), {"1990s": 1, "2000s": 1})


if __name__ == "__main__":
    unittest.main()
