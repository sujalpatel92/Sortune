"""
Wrapper for YouTube Music API (ytmusicapi or custom client).

This module acts as an anti-corruption layer: external responses are mapped
into core domain models (Track, Artist, Playlist).
"""

from sortune_core.models.playlist import Artist, Track


class YTMusicClient:
    def __init__(self):
        # Initialize ytmusicapi client here if needed.
        # Example:
        # from ytmusicapi import YTMusic
        # self.client = YTMusic("oauth.json")
        pass

    def sample_tracks(self) -> list[Track]:
        """
        Return a hardcoded list of demo tracks.
        Used for seeding in dev/demo environments.
        """
        return [
            Track(
                id="Y6FWFKXu1FY",
                title="Aap Ki Kashish",
                artists=[
                    Artist(name="Himesh Reshammiya"),
                    Artist(name="Krishna"),
                    Artist(name="Ahir"),
                ],
                album="Aashiq Banaya Aapne",
                in_library=False,
            )
        ]
