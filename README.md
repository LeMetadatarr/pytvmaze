# pytvmaze

TVmaze show catalog bulk harvester grouped onto the
[harvestkit](https://github.com/LeMetadatarr/harvestkit) resumable-harvest
engine. Extracted from [metadatarr](https://github.com/TigreGotico/metadatarr)'s
scraper collection into its own standalone package.

Also ships a real-time query client (`from pytvmaze import TVmazeClient`) alongside the bulk harvester.

## Sources

| Scraper | Registry name | Source |
| --- | --- | --- |
| `tvmaze_shows` | `tvmaze_shows` | TVmaze `/shows`, paginated (free, no auth) |

## Install

```bash
pip install pytvmaze
# or, for the HuggingFace publisher (via harvestkit):
pip install "pytvmaze[hf]"
# or, for Cloudflare-guarded sources:
pip install "pytvmaze[stealth]"
```

## Usage

```bash
# list every registered scraper
pytvmaze-harvest --list

# harvest the source (resumable — safe to Ctrl-C and rerun)
pytvmaze-harvest tvmaze_shows --output ~/.cache/metadatarr/scrapers/
```

Every scraper is a `harvestkit.engine.Source` subclass: checkpoint/dedup/
pagination/throttle are handled by the shared engine, each module only
answers `initial_cursor()` and `fetch(cursor)`. See
[harvestkit](https://github.com/LeMetadatarr/harvestkit) for the full engine
API.

## License

Apache-2.0
