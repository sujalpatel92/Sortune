"""
YouTube Music client (ytmusicapi) with a thin anti-corruption layer.

- Handles first-run OAuth and reuses a saved token file thereafter.
- Exposes read-only helpers:
    • list_library_playlists(limit=...) -> list[PlaylistSummary]
    • get_playlist_tracks(playlist_id, limit=...) -> list[Track]
- Maps external responses into core domain models (Track, Artist).

Env vars (see .env.example):
    YT_API_CLIENT_ID
    YT_API_CLIENT_SECRET
    YT_OAUTH_PATH (optional, defaults to .cache/ytmusic_oauth.json)
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, TypedDict

from dotenv import load_dotenv
from sortune_core.models.playlist import Artist, Track

load_dotenv()

log = logging.getLogger(__name__)


class PlaylistSummary(TypedDict, total=False):
    playlistId: str
    title: str
    count: int | None
    thumbnails: list | None


@dataclass(frozen=True)
class _Config:
    oauth_path: Path
    client_id: str | None
    client_secret: str | None


class YTMusicClient:
    """
    Thin wrapper around ytmusicapi that:
      - bootstraps OAuth on first run,
      - provides helpers to fetch library playlists and playlist tracks.
    """

    def __init__(
        self,
        oauth_path: Path | None = None,
        client_id: str | None = None,
        client_secret: str | None = None,
        open_browser: bool = True,
    ) -> None:
        self._cfg = _Config(
            oauth_path=oauth_path or Path(os.getenv("YT_OAUTH_PATH", "cache/ytmusic_oauth.json")),
            client_id=client_id or os.getenv("YT_API_CLIENT_ID") or None,
            client_secret=client_secret or os.getenv("YT_API_CLIENT_SECRET") or None,
        )
        self._open_browser = open_browser
        self._yt = None  # lazy

    # ---------- Public API ----------

    def list_library_playlists(self, limit: int = 200) -> list[PlaylistSummary]:
        """
        Return the user's library playlists (summary list).
        """
        yt = self._yt_client()
        items = yt.get_library_playlists(limit=limit)
        out: list[PlaylistSummary] = []
        for p in items:
            out.append(
                PlaylistSummary(
                    playlistId=p.get("playlistId"),
                    title=p.get("title"),
                    count=p.get("count"),
                    thumbnails=p.get("thumbnails"),
                )
            )
        return out

    def get_playlist_tracks(self, playlist_id: str, limit: int | None = None) -> list[Track]:
        """
        Return tracks for a playlist, mapped to core Track/Artist models.
        """
        yt = self._yt_client()
        raw = yt.get_playlist(playlistId=playlist_id, limit=limit)
        tracks = raw.get("tracks", []) or []
        return [self._to_track(t) for t in tracks]

    # Backward-compat demo data used elsewhere in the repo
    def sample_tracks(self) -> list[Track]:
        """
        Return a tiny, hardcoded list for seed/demo environments.
        """
        return [
            Track(
                id="Y6FWFKXu1FY",
                title="Aap Ki Kashish",
                artists=[
                    Artist(name="Himesh Reshammiya"),
                    Artist(name="Krishna"),
                    Artist(name="Ahir"),
                ],
                album="Aashiq Banaya Aapne",
                in_library=False,
            )
        ]

    # ---------- Internals ----------

    def _yt_client(self):
        """
        Lazy-initialize and return the underlying ytmusicapi client.
        Runs OAuth setup once if needed.
        """
        if self._yt is not None:
            return self._yt

        try:
            # local import to keep adapters import-safe
            from ytmusicapi import OAuthCredentials, YTMusic
        except Exception as e:
            raise RuntimeError(
                "ytmusicapi is not installed in the current environment. "
                "Add it to packages/adapters/pyproject.toml and reinstall."
            ) from e

        # Ensure OAuth token exists; if not, perform setup (opens browser by default).
        self._ensure_oauth(YTMusic)

        # Instantiate client from saved oauth json
        self._yt = YTMusic(
            str(self._cfg.oauth_path),
            oauth_credentials=OAuthCredentials(
                client_id=self._cfg.client_id, client_secret=self._cfg.client_secret
            ),
        )
        return self._yt

    def _ensure_oauth(self, YTMusic) -> None:
        """
        If the oauth json doesn't exist, run YTMusic.setup_oauth(...) once and save it.
        """
        path = self._cfg.oauth_path
        if path.exists():
            return

        path.parent.mkdir(parents=True, exist_ok=True)
        log.info("Running first-time OAuth for YouTube Music; saving credentials to %s", path)

        # Prefer explicit client id/secret if available (recommended).
        kwargs: dict[str, Any] = {"filepath": str(path), "open_browser": self._open_browser}
        if self._cfg.client_id and self._cfg.client_secret:
            kwargs["client_id"] = self._cfg.client_id
            kwargs["client_secret"] = self._cfg.client_secret

        try:
            YTMusic.setup_oauth(**kwargs)
        except Exception as e:
            # Clean up partial file if any
            if path.exists() and path.stat().st_size == 0:
                try:
                    path.unlink()
                except Exception:  # pragma: no cover
                    pass
            raise RuntimeError(
                "Failed to complete YouTube Music OAuth setup. "
                "Verify YT_API_CLIENT_ID / YT_API_CLIENT_SECRET in your environment "
                "or retry with a clean YT_OAUTH_PATH."
            ) from e

    @staticmethod
    def _to_track(t: dict[str, Any]) -> Track:
        """
        Convert a ytmusicapi track dict into our core Track model.
        ytmusicapi 'track' fields are not guaranteed stable; handle missing keys defensively.
        """
        video_id = t.get("videoId") or t.get("id") or ""
        title = t.get("title") or ""
        # Artists shape varies: [{"name": "...", "id": "..."}] or nested
        artists_raw = t.get("artists") or []
        artists = []
        for a in artists_raw:
            name = a.get("name") if isinstance(a, dict) else str(a)
            if name:
                artists.append(Artist(name=name))
        album = None
        album_obj = t.get("album")
        if isinstance(album_obj, dict):
            album = album_obj.get("name") or None
        elif isinstance(album_obj, str):
            album = album_obj
        in_library = bool(t.get("inLibrary") or t.get("in_library") or False)

        return Track(
            id=video_id,
            title=title,
            artists=artists,
            album=album,
            in_library=in_library,
        )
