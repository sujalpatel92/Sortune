from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from sortune_ai import PlaylistSuggestions, generate_playlist_name_suggestions

router = APIRouter(prefix="/ai", tags=["ai"])


class NameSuggestRequest(BaseModel):
    context: str = Field(..., description="Textual context like artists/albums/vibes/season")
    count: int = Field(5, ge=1, le=20, description="Number of suggestions to generate")
    seed: int | None = Field(None, description="Optional seed for determinism if supported")


@router.post("/suggest-playlist-names", response_model=PlaylistSuggestions)
def suggest_playlist_names(payload: NameSuggestRequest) -> PlaylistSuggestions:
    """Return AI-generated playlist name suggestions (validated schema)."""
    try:
        return generate_playlist_name_suggestions(
            context=payload.context, count=payload.count, seed=payload.seed
        )
    except ValueError as e:
        # Invalid JSON or schema from provider
        raise HTTPException(status_code=502, detail=str(e)) from e
    except Exception as e:  # pragma: no cover - safety net
        raise HTTPException(status_code=500, detail=str(e)) from e
