import pytest

try:
    import fakeredis
except Exception:  # pragma: no cover
    fakeredis = None

from sortune_adapters.storage.redis_repo import RedisPlaylistRepo
from sortune_core.models.playlist import Playlist


@pytest.mark.skipif(fakeredis is None, reason="fakeredis not installed")
def test_redis_repo_roundtrip():
    r = fakeredis.FakeRedis()
    repo = RedisPlaylistRepo(r)

    pl = Playlist.model_validate(
        {
            "playlistId": "demo",
            "title": "Demo Playlist",
            "tracks": [
                {
                    "videoId": "1",
                    "title": "A Song",
                    "artists": [{"name": "One"}],
                },
                {
                    "videoId": "2",
                    "title": "B Song",
                    "artists": [{"name": "Two"}],
                },
            ],
        }
    )

    # save -> get
    repo.save(pl)
    loaded = repo.get("demo")

    assert loaded.id == "demo"
    assert loaded.name == "Demo Playlist"
    assert [t.title for t in loaded.tracks] == ["A Song", "B Song"]


@pytest.mark.skipif(fakeredis is None, reason="fakeredis not installed")
def test_redis_repo_get_missing_returns_empty_playlist():
    r = fakeredis.FakeRedis()
    repo = RedisPlaylistRepo(r)

    loaded = repo.get("missing")
    assert loaded.id == "missing"
    assert loaded.tracks == []
