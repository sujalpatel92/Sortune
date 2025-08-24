from sortune_core.models.playlist import Artist, Track
from sortune_core.rules.simple import ByTitle


def test_by_title_sorts_case_insensitive():
    tracks = [
        Track(id="2", title="b Song", artists=[Artist(name="X")]),
        Track(id="1", title="A Song", artists=[Artist(name="X")]),
    ]
    out = list(ByTitle.apply(tracks))
    assert [t.title for t in out] == ["A Song", "b Song"]
