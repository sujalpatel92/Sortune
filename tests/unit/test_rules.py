from sortune_core.models.playlist import Track
from sortune_core.rules.simple import ByTitle


def test_by_title_sorts_case_insensitive():
    tracks = [
        Track.model_validate({"videoId": "2", "title": "b Song", "artists": [{"name": "X"}]}),
        Track.model_validate({"videoId": "1", "title": "A Song", "artists": [{"name": "X"}]}),
    ]
    out = list(ByTitle.apply(tracks))
    assert [t.title for t in out] == ["A Song", "b Song"]
