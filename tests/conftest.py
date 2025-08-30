import importlib

import pytest
from fastapi.testclient import TestClient
from sortune_api.main import app
from sortune_core.models.playlist import Playlist, Track

# Import the routes module once so we can override its dependency + YT client
playlists_module = importlib.import_module("sortune_api.routes.playlists")


class InMemoryPlaylistRepo:
    """Tiny in-memory stand-in for RedisPlaylistRepo used by the API routes."""

    def __init__(self):
        self.store: dict[str, Playlist] = {}

    # Matches the adapter's interface
    def get(self, playlist_id: str) -> Playlist:
        # Return an existing playlist or a placeholder so callers can mutate & save
        return self.store.get(
            playlist_id,
            Playlist.model_validate(
                {
                    "playlistId": playlist_id,
                    "title": f"Playlist {playlist_id}",
                    "tracks": [],
                }
            ),
        )

    def save(self, playlist: Playlist) -> None:
        self.store[playlist.id] = playlist

    def load_rule(self, name: str):
        from sortune_core.rules.simple import ByTitle

        if name == ByTitle.name:
            return ByTitle()
        raise ValueError(f"Unknown rule: {name}")


@pytest.fixture()
def repo() -> InMemoryPlaylistRepo:
    """Shared in-memory repo per-test."""
    return InMemoryPlaylistRepo()


@pytest.fixture()
def client(repo: InMemoryPlaylistRepo):
    """
    FastAPI TestClient using the real app, but with get_repo overridden
    to our in-memory repo. Seeds a small 'demo' playlist.
    """
    # Seed a sample playlist
    demo = Playlist.model_validate(
        {
            "playlistId": "demo",
            "title": "Demo",
            "tracks": [
                {
                    "videoId": "2",
                    "title": "b Song",
                    "artists": [{"name": "Artist"}],
                },
                {
                    "videoId": "1",
                    "title": "A Song",
                    "artists": [{"name": "Artist"}],
                },
            ],
        }
    )
    repo.save(demo)

    # Override the dependency inside the routes module
    app.dependency_overrides[playlists_module.get_repo] = lambda: repo
    try:
        yield TestClient(app)
    finally:
        # Clean up overrides so other tests don't leak state
        app.dependency_overrides.pop(playlists_module.get_repo, None)


@pytest.fixture()
def fake_yt(monkeypatch):
    """
    Monkeypatch the YTMusicClient used INSIDE the routes module so any call to
    /playlists/.../live uses this fake instead of hitting OAuth/network.
    """

    class FakeYT:
        def __init__(self, *_, **__):
            pass

        def list_library_playlists(self, limit: int = 200) -> list[dict]:
            items = [
                {"playlistId": "PL123", "title": "Road Trip", "count": 3, "thumbnails": []},
                {"playlistId": "PL999", "title": "Focus Mix", "count": 2, "thumbnails": []},
            ]
            return items[:limit]

        def get_playlist_tracks(self, playlist_id: str, limit: int | None = None) -> list[Track]:
            tracks_data = [
                {
                    "videoId": "vid1",
                    "title": "Song A",
                    "artists": [{"name": "Alice"}],
                    "album": {"name": "Alpha"},
                    "inLibrary": True,
                },
                {
                    "videoId": "vid2",
                    "title": "Song B",
                    "artists": [{"name": "Bob"}],
                    "album": {"name": "Beta"},
                    "inLibrary": False,
                },
            ]
            tracks = [Track.model_validate(t) for t in tracks_data]
            return tracks[:limit] if limit else tracks

    # IMPORTANT: patch the symbol as imported by the routes module
    monkeypatch.setattr(playlists_module, "YTMusicClient", lambda *a, **k: FakeYT())
    return FakeYT


@pytest.fixture()
def clear_yt_env(monkeypatch):
    """
    Ensure tests that rely on default naming aren't affected by user env.
    Clears YT_PLAYLIST_NAME by default; opt-in set it in a specific test if needed.
    """
    monkeypatch.delenv("YT_PLAYLIST_NAME", raising=False)
    yield
