# Datasets produced by pytvmaze

This repo harvests the TVmaze show catalog through the `/shows` endpoint. It produces one JSONL dataset where each row is a TV show or web series with schedule, network, rating, and external identifier information.

## Dataset format

Rows are written as JSON objects, one per line. One row per show.

| Field | Type | Description |
| --- | --- | --- |
| `tvmaze_id` | integer | TVmaze show identifier. |
| `name` | string / null | Show title. |
| `type` | string / null | Show type, for example `Scripted` or `Reality`. |
| `language` | string / null | Primary language. |
| `genres` | list of strings | Genre labels from TVmaze. |
| `status` | string / null | Production status, for example `Running` or `Ended`. |
| `runtime` | integer / null | Episode runtime in minutes. |
| `average_runtime` | integer / null | Average episode runtime in minutes. |
| `premiered` | string / null | First air date (`YYYY-MM-DD`). |
| `ended` | string / null | Final air date (`YYYY-MM-DD`). |
| `network_name` | string / null | Broadcasting network or streaming channel. |
| `network_country` | string / null | ISO country code of the network. |
| `rating_average` | float / null | Average user rating. |
| `schedule_time` | string / null | Typical air time. |
| `schedule_days` | list of strings | Typical air days. |
| `summary` | string / null | Plot summary with HTML tags removed. |
| `official_site` | string / null | Official show URL. |
| `imdb_id` | string / null | IMDb identifier. |
| `thetvdb_id` | integer / null | TheTVDB identifier. |
| `tvrage_id` | integer / null | TVRage identifier. |
| `image_medium` | string / null | URL to a medium-sized image. |

## How to generate

Install the package with the optional HuggingFace publisher support:

```bash
pip install "pytvmaze[hf]"
```

Run the harvester. No API key is required.

```bash
pytvmaze-harvest tvmaze_shows --output ~/.cache/metadatarr/scrapers/
```

The harvest is resumable. Stopping and rerunning the command continues from the last checkpoint kept in the output directory.

You can also run the source directly in Python:

```python
from pytvmaze.harvest.tvmaze_shows import TVMazeShowsSource

src = TVMazeShowsSource()
rows, cursor = src.fetch(0)
```

## Worth publishing on Hugging Face?

Yes. TVmaze data is available under a Creative Commons Attribution-ShareAlike license. A published snapshot gives the community a clean, structured TV show corpus with cross-references to IMDb and TheTVDB. Include the TVmaze attribution and license in the dataset card.

## ML tasks served

- TV show recommendation and similarity search.
- Genre and status classification.
- Schedule normalization and air-time prediction.
- Entity linking through `imdb_id`, `thetvdb_id`, and `tvrage_id`.
- Retrieval and RAG corpora for television queries.
