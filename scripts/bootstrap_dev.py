"""
Bootstrap a local dev environment by seeding a demo playlist into Redis.

Usage:
    uv run python scripts/bootstrap_dev.py
"""

import os

from redis import Redis
from sortune_adapters.storage.redis_repo import RedisPlaylistRepo
from sortune_adapters.ytmusic.client import YTMusicClient


def main(playlist_id: str = "demo"):
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    r = Redis.from_url(redis_url)
    repo = RedisPlaylistRepo(r)

    pl = repo.get(playlist_id)
    if not pl.tracks:
        pl.name = "Demo Playlist"
        pl.tracks = YTMusicClient().sample_tracks()
        repo.save(pl)
        print(f"Seeded {len(pl.tracks)} track(s) into playlist '{playlist_id}' at {redis_url}")
    else:
        print(f"Playlist '{playlist_id}' already has {len(pl.tracks)} track(s) at {redis_url}")


if __name__ == "__main__":
    main()
