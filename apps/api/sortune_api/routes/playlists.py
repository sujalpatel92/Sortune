from __future__ import annotations

import os

from fastapi import APIRouter, Depends, HTTPException, Query
from redis import Redis
from sortune_adapters.storage.redis_repo import RedisPlaylistRepo
from sortune_adapters.ytmusic.client import YTMusicClient
from sortune_core.models.playlist import Playlist, Track
from sortune_core.rules.simple import ByTitle

router = APIRouter(prefix="/playlists", tags=["playlists"])


def get_repo() -> RedisPlaylistRepo:
    r = Redis.from_url(os.getenv("REDIS_URL", "redis://redis:6379/0"))
    return RedisPlaylistRepo(r)


# ---------------- Storage-backed endpoints (unchanged behavior) ----------------


# ruff: noqa: B008
@router.get("/{playlist_id}", response_model=Playlist)
def get_playlist(playlist_id: str, repo: RedisPlaylistRepo = Depends(get_repo)):
    """Fetch a playlist from storage."""
    pl = repo.get(playlist_id)
    if not pl:
        raise HTTPException(status_code=404, detail="Playlist not found")
    return pl


# ruff: noqa: B008
@router.post("/{playlist_id}/sort")
def sort_playlist(
    playlist_id: str,
    rule_name: str = ByTitle.name,
    repo: RedisPlaylistRepo = Depends(get_repo),
):
    """Sort a playlist by the given rule and persist it."""
    pl = repo.get(playlist_id)
    if not pl:
        raise HTTPException(status_code=404, detail="Playlist not found")

    if rule_name == ByTitle.name:
        pl.tracks = list(ByTitle.apply(pl.tracks))
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported rule: {rule_name}")

    repo.save(pl)
    return {"status": "ok", "rule": rule_name, "count": len(pl.tracks)}


# ---------------- New YouTube Music live endpoints ----------------


# ruff: noqa: B008
@router.get("/library/live")
def list_yt_library_playlists(limit: int = Query(default=100, ge=1, le=500)):
    """
    Fetch the user's YouTube Music *library* playlists (live; not from Redis).
    Returns a compact summary list with playlistId/title/count/thumbnails.
    """
    try:
        client = YTMusicClient()
        return {"items": client.list_library_playlists(limit=limit)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


# ruff: noqa: B008
@router.get("/{playlist_id}/tracks/live", response_model=list[Track])
def get_yt_playlist_tracks_live(
    playlist_id: str,
    limit: int | None = Query(default=None, ge=1),
):
    """
    Fetch tracks for a YouTube Music playlist (live; not from Redis) and map to core Track.
    """
    try:
        client = YTMusicClient()
        return client.get_playlist_tracks(playlist_id=playlist_id, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


# ruff: noqa: B008
@router.post("/yt/import/{playlist_id}", response_model=Playlist, status_code=201)
def import_yt_playlist_into_redis(
    playlist_id: str,
    repo: RedisPlaylistRepo = Depends(get_repo),
    limit: int | None = Query(default=None, ge=1),
):
    """
    Import a YouTube Music playlist into Redis so local operations (like /sort) can run.

    Name resolution:
      - We don't pull the playlist title in the tracks call; use env YT_PLAYLIST_NAME
        if set, else fallback to 'YT:<id>'.
    """
    try:
        client = YTMusicClient()
        tracks = client.get_playlist_tracks(playlist_id=playlist_id, limit=limit)

        display_name = os.getenv("YT_PLAYLIST_NAME") or f"YT:{playlist_id}"
        playlist = Playlist(id=playlist_id, name=display_name, tracks=tracks)

        repo.save(playlist)
        return playlist
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


# ruff: noqa: B008
@router.post("/yt/refresh/{playlist_id}", response_model=Playlist)
def refresh_yt_playlist(
    playlist_id: str,
    repo: RedisPlaylistRepo = Depends(get_repo),
    limit: int | None = Query(default=None, ge=1),
):
    """
    Re-import a YouTube Music playlist and overwrite the stored copy in Redis.
    """
    try:
        client = YTMusicClient()
        tracks = client.get_playlist_tracks(playlist_id=playlist_id, limit=limit)
        display_name = os.getenv("YT_PLAYLIST_NAME") or f"YT:{playlist_id}"
        pl = Playlist(id=playlist_id, name=display_name, tracks=tracks)
        repo.save(pl)
        return pl
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
