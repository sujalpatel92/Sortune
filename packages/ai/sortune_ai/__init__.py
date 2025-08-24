"""
AI layer for Sortune.

Contains:
- Pydantic schemas for LLM output validation
- Prompt templates for playlist naming/curation
- Utilities for chaining with LangChain or direct API calls
"""
try:
    from ._version import __version__
except Exception:
    __version__ = "0.0.0"
from .schemas import PlaylistName, PlaylistSuggestions

__all__ = ["PlaylistName", "PlaylistSuggestions"]
