from ..models.playlist import Playlist
from ..repos.ports import PlaylistRepo, TrackRepo


class PlaylistService:
    """
    Application service for playlist operations.
    Wraps repository access + rule application in one place.
    """

    def __init__(self, tracks: TrackRepo, playlists: PlaylistRepo):
        self.tracks = tracks
        self.playlists = playlists

    def sort_playlist(self, playlist_id: str, rule_name: str) -> Playlist:
        """Apply a sorting rule to a playlist and persist the result."""
        pl = self.playlists.get(playlist_id)
        rule = self.playlists.load_rule(rule_name)
        pl.tracks = list(rule.apply(pl.tracks))
        self.playlists.save(pl)
        return pl
