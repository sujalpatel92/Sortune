from __future__ import annotations

import json
from typing import Any

from .config import load_llm_config
from .factory import get_llm
from .prompting import render_name_gen_prompt
from .schemas import PlaylistSuggestions


def generate_playlist_name_suggestions(
    *,
    context: str,
    count: int = 5,
    seed: int | None = None,
) -> PlaylistSuggestions:
    """
    Generate playlist name suggestions using the configured LLM provider.

    Returns a validated `PlaylistSuggestions` Pydantic model. Raises ValueError if
    the LLM output is not valid JSON or doesn't match the schema.
    """
    cfg = load_llm_config()
    llm = get_llm(cfg)

    # Build explicit JSON Schema for stronger guidance
    schema = PlaylistSuggestions.model_json_schema()
    prompt = render_name_gen_prompt(
        count=count, context=context, seed=seed or cfg.seed, json_schema=schema
    )
    # If backend supports response_format JSON schema (OpenAI), pass it through.
    model_kwargs = {
        "response_format": {
            "type": "json_schema",
            "json_schema": {"name": "PlaylistSuggestions", "schema": schema},
        }
    }
    raw = llm.generate(
        prompt,
        temperature=cfg.temperature,
        seed=seed or cfg.seed,
        model_kwargs=model_kwargs,
    )

    try:
        # Expect strict JSON per prompt instructions
        data: Any = json.loads(raw)
        return PlaylistSuggestions.model_validate(data)
    except Exception as e:
        raise ValueError("LLM did not return valid PlaylistSuggestions JSON") from e
