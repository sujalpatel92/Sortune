try:
    from ._version import __version__
except Exception:
    __version__ = "0.0.0"

from .models.playlist import Artist, Playlist, Track  # re-export core models

__all__ = ["Artist", "Track", "Playlist"]
