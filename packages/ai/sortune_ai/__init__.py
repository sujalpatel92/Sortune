"""
AI layer for Sortune.

Contains:
- Pydantic schemas for LLM output validation
- Prompt templates for playlist naming/curation
- Utilities for chaining with LangChain or direct API calls
"""

from .schemas import PlaylistName, PlaylistSuggestions

__all__ = ["PlaylistName", "PlaylistSuggestions"]
