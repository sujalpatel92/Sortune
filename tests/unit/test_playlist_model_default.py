from sortune_core.models.playlist import Playlist, Track


def test_playlist_tracks_default_not_shared() -> None:
    a = Playlist.model_validate({"playlistId": "A", "title": "One"})
    b = Playlist.model_validate({"playlistId": "B", "title": "Two"})

    a.tracks.append(
        Track.model_validate({"videoId": "x", "title": "X", "artists": [{"name": "Z"}]})
    )
    assert len(a.tracks) == 1
    assert len(b.tracks) == 0  # proves the default list isn't shared
