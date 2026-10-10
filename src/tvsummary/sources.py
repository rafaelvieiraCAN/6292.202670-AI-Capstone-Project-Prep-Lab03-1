"""Remote data retrieval. This is the only module that imports requests."""

import requests

from .config import REQUEST_TIMEOUT, SOURCE_URL
from .models import ShowRecord


class TVMazeSource:
    """Fetch TVMaze show records and convert them to ShowRecord objects."""

    def __init__(self, url: str = SOURCE_URL, timeout: int = REQUEST_TIMEOUT):
        """Store the endpoint and request timeout."""
        self.url = url
        self.timeout = timeout

    def fetch_records(self) -> list[ShowRecord]:
        """Download the endpoint and return normalized show records."""
        response = requests.get(self.url, timeout=self.timeout)
        response.raise_for_status()
        payload = response.json()
        if not isinstance(payload, list):
            raise ValueError("TVMaze response was not a list of show records.")
        return [ShowRecord(item) for item in payload]
