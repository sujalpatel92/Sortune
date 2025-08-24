import pytest
from fastapi.testclient import TestClient
from sortune_api.main import app
from sortune_api.routes.playlists import get_repo
from sortune_core.models.playlist import Artist, Playlist, Track


class InMemoryPlaylistRepo:
    def __init__(self):
        self.store: dict[str, Playlist] = {}

    # Matches the adapter's interface
    def get(self, playlist_id: str) -> Playlist:
        return self.store.get(
            playlist_id, Playlist(id=playlist_id, name=f"Playlist {playlist_id}", tracks=[])
        )

    def save(self, playlist: Playlist) -> None:
        self.store[playlist.id] = playlist

    def load_rule(self, name: str):
        from sortune_core.rules.simple import ByTitle

        if name == ByTitle.name:
            return ByTitle()
        raise ValueError(f"Unknown rule: {name}")


@pytest.fixture()
def client():
    # Set up in-memory repo and override the dependency
    repo = InMemoryPlaylistRepo()

    # Seed a sample playlist
    demo = Playlist(
        id="demo",
        name="Demo",
        tracks=[
            Track(id="2", title="b Song", artists=[Artist(name="Artist")]),
            Track(id="1", title="A Song", artists=[Artist(name="Artist")]),
        ],
    )
    repo.save(demo)

    app.dependency_overrides[get_repo] = lambda: repo
    try:
        yield TestClient(app)
    finally:
        # Clean up overrides
        app.dependency_overrides.pop(get_repo, None)
