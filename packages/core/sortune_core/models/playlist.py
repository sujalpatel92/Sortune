from pydantic import BaseModel, Field, model_validator


class Artist(BaseModel):
    name: str
    id: str | None = None
    browseId: str | None = None
    shuffleId: str | None = None
    radioId: str | None = None
    subscribers: str | None = None
    thumbnails: list[dict] | None = None
    artist: str | None = None  # to capture artist name from artist_data

    @model_validator(mode="before")
    def _unify_fields(cls, values):
        if not isinstance(values, dict):
            return values
        # Unify name and artist
        if values.get("artist") and not values.get("name"):
            values["name"] = values["artist"]
        # Unify id and browseId
        if values.get("browseId") and not values.get("id"):
            values["id"] = values["browseId"]
        return values


class Author(BaseModel):
    name: str
    id: str | None = None


class Album(BaseModel):
    name: str
    id: str | None = None
    browseId: str | None = None
    playlistId: str | None = None
    thumbnails: list[dict] | None = None
    type: str | None = None
    artists: list[Artist] | None = None
    year: str | None = None
    title: str | None = None  # to capture title from album_data

    @model_validator(mode="before")
    def _unify_fields(cls, values):
        if not isinstance(values, dict):
            return values
        # Unify name and title
        if values.get("title") and not values.get("name"):
            values["name"] = values["title"]
        # Unify id and browseId
        if values.get("browseId") and not values.get("id"):
            values["id"] = values["browseId"]
        return values


class Track(BaseModel):
    id: str = Field(..., alias="videoId")
    title: str
    artists: list[Artist]
    album: Album | None = None
    duration_seconds: int | None = Field(None, alias="duration_seconds")
    like_status: str | None = Field(None, alias="likeStatus")
    in_library: bool = Field(False, alias="inLibrary")


class Playlist(BaseModel):
    id: str = Field(..., alias="playlistId")
    name: str = Field(..., alias="title")
    author: list[Author] | None = None
    description: str | None = None
    count: str | None = None
    thumbnails: list[dict] | None = None
    # IMPORTANT: avoid shared mutable default list across instances
    tracks: list[Track] = Field(default_factory=list)
