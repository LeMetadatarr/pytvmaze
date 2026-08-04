"""pytvmaze — TVmaze show catalog bulk harvester, grouped on harvestkit.

Importing this package imports :mod:`pytvmaze.harvest`, which in turn
imports the scraper module so it registers itself with
:mod:`harvestkit.engine` (``@register``).
"""
from pytvmaze.version import __version__

import pytvmaze.harvest  # noqa: F401  (import for @register side effects)

from pytvmaze.client import TVmazeClient
from pytvmaze.models import (
    TVmazeNetwork,
    TVmazeExternals,
    TVmazeShow,
    TVmazePerson,
    TVmazeSeason,
    TVmazeCastMember,
)

__all__ = [
    "__version__",
    "TVmazeClient",
    "TVmazeNetwork",
    "TVmazeExternals",
    "TVmazeShow",
    "TVmazePerson",
    "TVmazeSeason",
    "TVmazeCastMember",
]
