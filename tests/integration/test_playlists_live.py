from __future__ import annotations

from fastapi.testclient import TestClient
from sortune_core.models.playlist import Playlist


def test_list_yt_library_playlists_live_ok(client: TestClient, fake_yt) -> None:
    resp = client.get("/playlists/library/live")
    assert resp.status_code == 200
    body = resp.json()
    assert "items" in body
    assert len(body["items"]) == 2
    assert body["items"][0]["playlistId"] == "PL123"
    assert body["items"][0]["title"] == "Road Trip"


def test_get_yt_playlist_tracks_live_ok(client: TestClient, fake_yt) -> None:
    resp = client.get("/playlists/PL123/tracks/live")
    assert resp.status_code == 200
    tracks = resp.json()
    assert isinstance(tracks, list)
    assert tracks[0]["id"] == "vid1"
    assert tracks[0]["title"] == "Song A"
    assert tracks[0]["artists"][0]["name"] == "Alice"
    assert tracks[0]["album"] == "Alpha"
    assert tracks[0]["in_library"] is True


def test_import_yt_playlist_into_redis_persists(
    client: TestClient, fake_yt, repo, clear_yt_env
) -> None:
    resp = client.post("/playlists/yt/import/PL123")
    assert resp.status_code == 201
    pl = resp.json()
    assert pl["id"] == "PL123"
    assert pl["name"] == "YT:PL123"  # default fallback name
    assert len(pl["tracks"]) == 2

    # Verify persisted in the in-memory repo fixture
    stored = repo.get("PL123")
    assert isinstance(stored, Playlist)
    assert stored.name == "YT:PL123"
    assert len(stored.tracks) == 2


def test_import_with_env_name_override(client: TestClient, fake_yt, repo, monkeypatch) -> None:
    monkeypatch.setenv("YT_PLAYLIST_NAME", "My Fav Tracks")
    resp = client.post("/playlists/yt/import/PL123")
    assert resp.status_code == 201
    pl = resp.json()
    assert pl["name"] == "My Fav Tracks"
