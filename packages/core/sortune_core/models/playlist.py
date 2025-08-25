from pydantic import BaseModel, Field


class Artist(BaseModel):
    name: str
    id: str | None = None


class Track(BaseModel):
    id: str
    title: str
    artists: list[Artist]
    album: str | None = None
    duration_ms: int | None = None
    like_status: str | None = None
    in_library: bool = False


class Playlist(BaseModel):
    id: str
    name: str
    description: str | None = None
    # IMPORTANT: avoid shared mutable default list across instances
    tracks: list[Track] = Field(default_factory=list)
