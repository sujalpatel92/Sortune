from sortune_core.models.playlist import Playlist


def test_playlist_model_validation():
    pl = Playlist.model_validate(
        {
            "playlistId": "demo",
            "title": "Demo Playlist",
            "tracks": [
                {
                    "videoId": "1",
                    "title": "Test",
                    "artists": [{"name": "Tester"}],
                }
            ],
        }
    )
    assert pl.id == "demo"
    assert pl.tracks[0].title == "Test"
    assert pl.tracks[0].artists[0].name == "Tester"
