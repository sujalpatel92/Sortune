"""
Demo job: backfill a small playlist with sample tracks.

This is used by the Streamlit UI "Seed demo" button and can also be enqueued
onto an RQ queue if you wire a producer.
"""

from redis import Redis
from sortune_adapters.storage.redis_repo import RedisPlaylistRepo
from sortune_adapters.ytmusic.client import YTMusicClient


def backfill_demo_playlist():
    """
    Idempotent: if 'demo' already has tracks, it won't duplicate.
    Returns a tiny status dict for UI/debugging.
    """
    r = Redis.from_url("redis://redis:6379/0")
    repo = RedisPlaylistRepo(r)

    pl = repo.get("demo")
    if not pl.tracks:
        pl.name = "Demo Playlist"
        pl.tracks = YTMusicClient().sample_tracks()
        repo.save(pl)

    return {"playlist": pl.id, "tracks": len(pl.tracks)}
