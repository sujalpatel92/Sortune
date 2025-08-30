"""
Imports user's YouTube Music playlists into Sortune.

- Fetches all library playlists.
- Filters out playlists authored by "YouTube Music".
- Saves the remaining playlists and their tracks to Redis.
"""

import logging
import os

from redis import Redis
from sortune_adapters.storage.redis_repo import RedisPlaylistRepo
from sortune_adapters.ytmusic.client import YTMusicClient
from sortune_core.models.playlist import Playlist

log = logging.getLogger(__name__)


def main():
    logging.basicConfig(level=logging.INFO)

    # Initialize clients
    yt_client = YTMusicClient()
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    r = Redis.from_url(redis_url)
    redis_repo = RedisPlaylistRepo(r)

    # Fetch playlists
    log.info("Fetching library playlists from YouTube Music...")
    playlists = yt_client.list_library_playlists(limit=500)  # Increased limit
    log.info(f"Found {len(playlists)} total playlists.")

    # Filter and save
    saved_count = 0
    for p_summary in playlists:
        authors = p_summary.get("author")
        if authors and any(author.get("name") == "YouTube Music" for author in authors):
            log.info(f"Skipping playlist from 'YouTube Music': {p_summary['title']}")
            continue

        playlist_id = p_summary["playlistId"]
        log.info(f"Importing playlist: {p_summary['title']} ({playlist_id})")

        try:
            tracks = yt_client.get_playlist_tracks(playlist_id)
            playlist = Playlist.model_validate(p_summary)
            playlist.tracks = tracks
            redis_repo.save(playlist)
            saved_count += 1
            log.info(f"  ...saved with {len(tracks)} tracks.")
        except Exception as e:
            log.error(f"Could not import playlist {p_summary['title']}: {e}")

    log.info(f"Successfully imported {saved_count} playlists to Redis.")


if __name__ == "__main__":
    main()
