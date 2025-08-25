from sortune_adapters.ytmusic.client import YTMusicClient
from sortune_core.models.playlist import Track


def test_to_track_maps_common_shape() -> None:
    raw = {
        "videoId": "abc123",
        "title": "Test Song",
        "artists": [{"name": "Artist One"}, {"name": "Artist Two"}],
        "album": {"name": "Album X"},
        "inLibrary": True,
    }
    t: Track = YTMusicClient._to_track(raw)
    assert t.id == "abc123"
    assert t.title == "Test Song"
    assert [a.name for a in t.artists] == ["Artist One", "Artist Two"]
    assert t.album == "Album X"
    assert t.in_library is True


def test_to_track_handles_artists_as_strings_and_album_as_string() -> None:
    raw = {
        "videoId": "zzz999",
        "title": "Loose Data",
        "artists": ["Solo Artist"],  # be defensive
        "album": "Loose Album",
        # no inLibrary -> default False
    }
    t: Track = YTMusicClient._to_track(raw)
    assert t.id == "zzz999"
    assert [a.name for a in t.artists] == ["Solo Artist"]
    assert t.album == "Loose Album"
    assert t.in_library is False


def test_to_track_respects_in_library_alias() -> None:
    raw = {"videoId": "id42", "title": "Alias Field", "artists": [], "in_library": True}
    t: Track = YTMusicClient._to_track(raw)
    assert t.in_library is True
