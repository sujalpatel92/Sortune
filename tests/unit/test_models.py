from sortune_core.models.playlist import Artist, Playlist, Track


def test_playlist_model_validation():
    pl = Playlist(
        id="demo",
        name="Demo Playlist",
        tracks=[Track(id="1", title="Test", artists=[Artist(name="Tester")])],
    )
    assert pl.id == "demo"
    assert pl.tracks[0].title == "Test"
    assert pl.tracks[0].artists[0].name == "Tester"
