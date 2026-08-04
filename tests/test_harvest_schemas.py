"""Row-schema equivalence tests for the TVmaze scraper.

Relocated verbatim (assertions untouched) from metadatarr's
test_scrapers_batch1.py, keeping only the tests for the scraper that lives in
this package, re-pointed at pytvmaze.harvest.*. These lock the exact flat-row
shape the scraper emits (the contract the LeData datasets depend on)
against a realistic upstream sample, so a future engine change can't
silently alter the output schema.
"""
from __future__ import annotations

from harvestkit.engine import all_sources

from pytvmaze.harvest.tvmaze_shows import TVMazeShowsSource


def test_tvmaze_shows_map_row_schema():
    src = TVMazeShowsSource()
    s = {
        "id": 1,
        "name": "Under the Dome",
        "type": "Scripted",
        "language": "English",
        "genres": ["Drama", "Science-Fiction"],
        "status": "Ended",
        "runtime": 60,
        "averageRuntime": 60,
        "premiered": "2013-06-24",
        "ended": "2015-09-10",
        "network": {"name": "CBS", "country": {"code": "US"}},
        "rating": {"average": 6.5},
        "schedule": {"time": "22:00", "days": ["Thursday"]},
        "summary": "<p>Small town.</p>",
        "officialSite": "http://example.com",
        "externals": {"imdb": "tt1553656", "thetvdb": 153021, "tvrage": 25988},
        "image": {"medium": "http://example.com/med.jpg"},
    }
    row = src.map_row(s)
    assert row["tvmaze_id"] == 1
    assert row["summary"] == "Small town."
    assert row["network_name"] == "CBS"
    assert row["network_country"] == "US"
    assert set(row) == {
        "tvmaze_id", "name", "type", "language", "genres", "status",
        "runtime", "average_runtime", "premiered", "ended", "network_name",
        "network_country", "rating_average", "schedule_time",
        "schedule_days", "summary", "official_site", "imdb_id",
        "thetvdb_id", "tvrage_id", "image_medium",
    }


def test_tvmaze_shows_fetch_stops_on_404(monkeypatch):
    src = TVMazeShowsSource()

    class FakeResp:
        status_code = 404

    class FakeSession:
        def get(self, *a, **kw):
            return FakeResp()

    src._session = FakeSession()
    src.throttle.wait = lambda: None
    rows, cursor = src.fetch(5)
    assert rows == []
    assert cursor is None


def test_pytvmaze_scraper_is_registered():
    reg = all_sources()
    assert reg.get("tvmaze_shows") is TVMazeShowsSource
