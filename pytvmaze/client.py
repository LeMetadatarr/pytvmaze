from typing import Dict, List, Optional, Union

from .version import __version__
from .transport import make_session

# Canonical user-agent string for this client. Keeping this in one place
# means a version bump doesn't need to touch the client constructor.
_USER_AGENT = f"pytvmaze/{__version__}"

from .models import (
    TVmazeShow,
    TVmazeSeason,
    TVmazeCastMember,
    TVmazePerson,
)


class TVmazeClient:
    """Client for the TVmaze public API (https://www.tvmaze.com/api).

    No authentication or API key required.  Rate limit is 20 requests per 10
    seconds for unauthenticated clients.
    """

    BASE = "https://api.tvmaze.com"

    def __init__(self, user_agent: str = _USER_AGENT):
        self._session = make_session()
        self._session.headers["User-Agent"] = user_agent
        self._session.headers["Accept"] = "application/json"

    def _get(self, path: str, **params) -> Optional[Union[Dict, List]]:
        try:
            r = self._session.get(f"{self.BASE}{path}", params=params or None, timeout=10)
            if r.status_code == 404:
                return None
            r.raise_for_status()
            return r.json()
        except Exception:
            return None

    # ------------------------------------------------------------------
    # Show search & lookup
    # ------------------------------------------------------------------

    def search_shows(self, query: str) -> List[TVmazeShow]:
        data = self._get("/search/shows", q=query)
        if not isinstance(data, list):
            return []
        return [TVmazeShow.model_validate(item["show"]) for item in data if "show" in item]

    def singlesearch(self, query: str) -> Optional[TVmazeShow]:
        data = self._get("/singlesearch/shows", q=query)
        return TVmazeShow.model_validate(data) if isinstance(data, dict) else None

    def get_show(self, tvmaze_id: int) -> Optional[TVmazeShow]:
        data = self._get(f"/shows/{tvmaze_id}")
        return TVmazeShow.model_validate(data) if isinstance(data, dict) else None

    def lookup_by_thetvdb(self, thetvdb_id: int) -> Optional[TVmazeShow]:
        data = self._get("/lookup/shows", thetvdb=thetvdb_id)
        return TVmazeShow.model_validate(data) if isinstance(data, dict) else None

    def lookup_by_imdb(self, imdb_id: str) -> Optional[TVmazeShow]:
        data = self._get("/lookup/shows", imdb=imdb_id)
        return TVmazeShow.model_validate(data) if isinstance(data, dict) else None

    # ------------------------------------------------------------------
    # Seasons & cast
    # ------------------------------------------------------------------

    def get_seasons(self, tvmaze_id: int) -> List[TVmazeSeason]:
        data = self._get(f"/shows/{tvmaze_id}/seasons")
        if not isinstance(data, list):
            return []
        return [TVmazeSeason.model_validate(s) for s in data]

    def get_cast(self, tvmaze_id: int) -> List[TVmazeCastMember]:
        data = self._get(f"/shows/{tvmaze_id}/cast")
        if not isinstance(data, list):
            return []
        return [TVmazeCastMember.model_validate(m) for m in data]

    # ------------------------------------------------------------------
    # People
    # ------------------------------------------------------------------

    def search_people(self, query: str) -> List[TVmazePerson]:
        data = self._get("/search/people", q=query)
        if not isinstance(data, list):
            return []
        return [TVmazePerson.model_validate(item["person"]) for item in data if "person" in item]
