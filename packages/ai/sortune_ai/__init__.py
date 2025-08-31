"""
AI layer for Sortune.

Contains:
- Pydantic schemas for LLM output validation
- Prompt templates for playlist naming/curation
- Provider-agnostic BaseLLM interface and factory
- Convenience helpers to generate playlist name suggestions
"""

from __future__ import annotations

try:
    from ._version import __version__
except Exception:  # pragma: no cover - fallback in non-built environments
    __version__ = "0.0.0"

from .base import BaseLLM
from .config import LLMConfig, load_llm_config
from .factory import get_llm
from .playlist_namer import generate_playlist_name_suggestions
from .schemas import PlaylistName, PlaylistSuggestions

__all__ = [
    "__version__",
    # Schemas
    "PlaylistName",
    "PlaylistSuggestions",
    # LLM
    "BaseLLM",
    "LLMConfig",
    "load_llm_config",
    "get_llm",
    # Helpers
    "generate_playlist_name_suggestions",
]
