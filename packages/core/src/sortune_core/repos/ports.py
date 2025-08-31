from collections.abc import Iterable
from typing import Protocol

from ..models.playlist import Playlist, Track


class TrackRepo(Protocol):
    def by_playlist(self, playlist_id: str) -> Iterable[Track]:
        """Return tracks for a given playlist."""
        ...

    def upsert(self, tracks: Iterable[Track]) -> None:
        """Insert or update tracks in storage."""
        ...


class PlaylistRepo(Protocol):
    def get(self, playlist_id: str) -> Playlist:
        """Fetch a playlist by ID."""
        ...

    def save(self, playlist: Playlist) -> None:
        """Persist a playlist."""
        ...

    def load_rule(self, name: str):
        """Return a callable rule object by name."""
        ...
