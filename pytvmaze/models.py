"""Pydantic models returned by :class:`pytvmaze.client.TVmazeClient`.

Extracted verbatim from metadatarr's ``models.py`` (TVmaze* classes). This
module has no dependency on metadatarr.
"""
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict, model_validator


class TVmazeNetwork(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: Optional[int] = None
    name: Optional[str] = None
    country_code: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def _flatten(cls, v):
        if isinstance(v, dict):
            v = dict(v)
            country = v.pop("country", None) or {}
            if isinstance(country, dict):
                v.setdefault("country_code", country.get("code"))
        return v


class TVmazeExternals(BaseModel):
    model_config = ConfigDict(extra="ignore")
    tvrage: Optional[int] = None
    thetvdb: Optional[int] = None
    imdb: Optional[str] = None


class TVmazeShow(BaseModel):
    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    id: int
    name: str
    url: Optional[str] = None
    show_type: Optional[str] = Field(None, alias="type")
    language: Optional[str] = None
    genres: List[str] = Field(default_factory=list)
    status: Optional[str] = None
    runtime: Optional[int] = None
    average_runtime: Optional[int] = Field(None, alias="averageRuntime")
    premiered: Optional[str] = None
    ended: Optional[str] = None
    official_site: Optional[str] = Field(None, alias="officialSite")
    rating: Optional[float] = None
    network: Optional[TVmazeNetwork] = None
    web_channel: Optional[TVmazeNetwork] = Field(None, alias="webChannel")
    externals: Optional[TVmazeExternals] = None
    image_medium: Optional[str] = None
    image_original: Optional[str] = None
    summary: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def _flatten(cls, v):
        if isinstance(v, dict):
            v = dict(v)
            img = v.pop("image", None) or {}
            v.setdefault("image_medium", img.get("medium"))
            v.setdefault("image_original", img.get("original"))
            rating = v.get("rating")
            if isinstance(rating, dict):
                v["rating"] = rating.get("average")
        return v


class TVmazePerson(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: int
    name: str
    url: Optional[str] = None
    birthday: Optional[str] = None
    deathday: Optional[str] = None
    gender: Optional[str] = None
    country_code: Optional[str] = None
    image_medium: Optional[str] = None
    image_original: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def _flatten(cls, v):
        if isinstance(v, dict):
            v = dict(v)
            img = v.pop("image", None) or {}
            country = v.pop("country", None) or {}
            v.setdefault("image_medium", img.get("medium"))
            v.setdefault("image_original", img.get("original"))
            v.setdefault("country_code", country.get("code"))
        return v


class TVmazeSeason(BaseModel):
    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    id: int
    number: int
    name: Optional[str] = None
    episode_order: Optional[int] = Field(None, alias="episodeOrder")
    premiere_date: Optional[str] = Field(None, alias="premiereDate")
    end_date: Optional[str] = Field(None, alias="endDate")
    image_medium: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def _flatten(cls, v):
        if isinstance(v, dict):
            v = dict(v)
            img = v.pop("image", None) or {}
            v.setdefault("image_medium", img.get("medium"))
        return v


class TVmazeCastMember(BaseModel):
    model_config = ConfigDict(extra="ignore")

    person: Optional[TVmazePerson] = None
    character_name: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def _flatten(cls, v):
        if isinstance(v, dict):
            v = dict(v)
            char = v.pop("character", None) or {}
            v.setdefault("character_name", char.get("name"))
        return v
