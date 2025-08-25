import os
import sys

from dotenv import load_dotenv
from redis import Redis
from sortune_adapters.storage.redis_repo import RedisPlaylistRepo
from sortune_adapters.ytmusic.client import YTMusicClient
from sortune_core.models.playlist import Playlist

load_dotenv()

if __name__ == "__main__":
    pid = os.getenv("YT_PLAYLIST_ID") or (sys.argv[1] if len(sys.argv) > 1 else None)
    if not pid:
        print("Usage: YT_PLAYLIST_ID=<id> python scripts/import_yt.py")
        raise SystemExit(2)
    r = Redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379/0"))
    repo = RedisPlaylistRepo(r)
    tracks = YTMusicClient().get_playlist_tracks(pid)
    name = os.getenv("YT_PLAYLIST_NAME") or f"YT:{pid}"
    repo.save(Playlist(id=pid, name=name, tracks=tracks))
    print(f"Imported {len(tracks)} tracks into Redis as {name}")
