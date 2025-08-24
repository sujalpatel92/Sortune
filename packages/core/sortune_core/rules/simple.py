from collections.abc import Iterable

from ..models.playlist import Track


class ByTitle:
    """Sort tracks alphabetically by title (case-insensitive)."""

    name = "by_title"

    @staticmethod
    def apply(tracks: Iterable[Track]) -> Iterable[Track]:
        return sorted(tracks, key=lambda t: t.title.lower())
