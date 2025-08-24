from fastapi import APIRouter, Depends, HTTPException
from redis import Redis
from sortune_adapters.storage.redis_repo import RedisPlaylistRepo
from sortune_core.models.playlist import Playlist
from sortune_core.rules.simple import ByTitle

router = APIRouter(prefix="/playlists", tags=["playlists"])


def get_repo() -> RedisPlaylistRepo:
    r = Redis.from_url("redis://redis:6379/0")
    return RedisPlaylistRepo(r)


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
