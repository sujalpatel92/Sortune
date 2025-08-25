from sortune_core.models.playlist import Artist, Playlist, Track


def test_playlist_tracks_default_not_shared() -> None:
    a = Playlist(id="A", name="One")
    b = Playlist(id="B", name="Two")

    a.tracks.append(Track(id="x", title="X", artists=[Artist(name="Z")]))
    assert len(a.tracks) == 1
    assert len(b.tracks) == 0  # proves the default list isn't shared
