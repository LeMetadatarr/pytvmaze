"""Network-free smoke test for the real-time TVmaze query client.

The client's ``_get`` is monkeypatched to return a captured sample API
response, so parsing is exercised without ever touching the network.
"""
from __future__ import annotations

from pytvmaze import TVmazeClient, TVmazeShow, TVmazeSeason, TVmazeCastMember

_SAMPLE_SHOW = {
    "id": 1,
    "name": "Under the Dome",
    "type": "Scripted",
    "language": "English",
    "genres": ["Drama", "Science-Fiction"],
    "status": "Ended",
    "runtime": 60,
    "premiered": "2013-06-24",
    "ended": "2015-09-10",
    "network": {"name": "CBS", "country": {"code": "US"}},
    "image": {"medium": "http://example.com/m.jpg", "original": "http://example.com/o.jpg"},
    "externals": {"tvrage": 25988, "thetvdb": 264492, "imdb": "tt1553656"},
    "summary": "<p>Small town, big dome.</p>",
}

_SAMPLE_SEASON = {
    "id": 1, "number": 1, "name": "Season 1",
    "episodeOrder": 13, "premiereDate": "2013-06-24", "endDate": "2013-09-16",
    "image": {"medium": "http://example.com/s1.jpg"},
}

_SAMPLE_CAST = {
    "person": {"id": 10, "name": "Mike Vogel", "country": {"code": "US"}},
    "character": {"id": 20, "name": "Dale Barbara"},
}


def _client_with_fake_get(payload):
    client = TVmazeClient()

    def _fake_get(path, **params):
        return payload

    client._get = _fake_get
    return client


def test_singlesearch_parses_show():
    client = _client_with_fake_get(_SAMPLE_SHOW)
    show = client.singlesearch("under the dome")
    assert isinstance(show, TVmazeShow)
    assert show.id == 1
    assert show.name == "Under the Dome"
    assert show.network.name == "CBS"
    assert show.externals.imdb == "tt1553656"


def test_search_shows_unwraps_list():
    client = _client_with_fake_get([{"show": _SAMPLE_SHOW}])
    shows = client.search_shows("dome")
    assert len(shows) == 1
    assert shows[0].id == 1
    assert shows[0].image_medium == "http://example.com/m.jpg"


def test_get_seasons_parses_list():
    client = _client_with_fake_get([_SAMPLE_SEASON])
    seasons = client.get_seasons(1)
    assert len(seasons) == 1
    assert isinstance(seasons[0], TVmazeSeason)
    assert seasons[0].episode_order == 13


def test_get_cast_parses_list():
    client = _client_with_fake_get([_SAMPLE_CAST])
    cast = client.get_cast(1)
    assert len(cast) == 1
    assert isinstance(cast[0], TVmazeCastMember)
    assert cast[0].person.name == "Mike Vogel"
    assert cast[0].character_name == "Dale Barbara"
