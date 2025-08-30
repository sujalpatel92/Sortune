import json
from pathlib import Path

from sortune_core.models.playlist import Album, Artist, Playlist, Track


def test_load_playlist_data():
    path = Path("playlist_data_example.json")
    data = json.loads(path.read_text())
    for item in data:
        Playlist.model_validate(item)


def test_load_track_data():
    path = Path("track_data_example.json")
    data = json.loads(path.read_text())
    for item in data:
        Track.model_validate(item)


def test_load_album_data():
    path = Path("album_data_example.json")
    data = json.loads(path.read_text())
    for item in data:
        Album.model_validate(item)


def test_load_artist_data():
    path = Path("artist_data_example.json")
    data = json.loads(path.read_text())
    for item in data:
        Artist.model_validate(item)
