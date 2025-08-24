"""
Redis-backed implementation of PlaylistRepo.
Stores playlists as JSON blobs keyed by playlist ID.
"""

import json

from redis import Redis
from sortune_core.models.playlist import Playlist


class RedisPlaylistRepo:
    def __init__(self, redis: Redis):
        self.r = redis

    def _key(self, pid: str) -> str:
        return f"playlist:{pid}"

    def get(self, playlist_id: str) -> Playlist:
        raw = self.r.get(self._key(playlist_id))
        if not raw:
            # Return an empty playlist if nothing exists
            return Playlist(id=playlist_id, name=f"Playlist {playlist_id}", tracks=[])
        data = json.loads(raw)
        return Playlist.model_validate(data)

    def save(self, playlist: Playlist) -> None:
        self.r.set(self._key(playlist.id), playlist.model_dump_json())

    def load_rule(self, name: str):
        # Simple inline registry for now
        from sortune_core.rules.simple import ByTitle

        if name == ByTitle.name:
            return ByTitle()
        raise ValueError(f"Unknown rule: {name}")
