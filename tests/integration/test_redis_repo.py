import pytest

try:
    import fakeredis
except Exception:  # pragma: no cover
    fakeredis = None

from sortune_adapters.storage.redis_repo import RedisPlaylistRepo
from sortune_core.models.playlist import Artist, Playlist, Track


@pytest.mark.skipif(fakeredis is None, reason="fakeredis not installed")
def test_redis_repo_roundtrip():
    r = fakeredis.FakeRedis()
    repo = RedisPlaylistRepo(r)

    pl = Playlist(
        id="demo",
        name="Demo Playlist",
        tracks=[
            Track(id="1", title="A Song", artists=[Artist(name="One")]),
            Track(id="2", title="B Song", artists=[Artist(name="Two")]),
        ],
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
