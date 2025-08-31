from __future__ import annotations

import json
from pathlib import Path

PROMPTS_DIR = Path(__file__).parent / "prompts"


def render_name_gen_prompt(
    *, count: int, context: str, seed: int | None = None, json_schema: dict | None = None
) -> str:
    """
    Render the playlist name generation prompt with optional seed hint.

    The underlying models may support a true 'seed' parameter; we also inject a
    textual seed hint to encourage stable style across providers.
    """
    tpl_path = PROMPTS_DIR / "name_gen.md"
    base = tpl_path.read_text(encoding="utf-8")
    prompt = base.format(count=count, context=context)
    if seed is not None:
        prompt = f"{prompt}\n\nSEED_HINT: {seed}"
    if json_schema is not None:
        schema_str = json.dumps(json_schema, indent=2)
        prompt = (
            f"{prompt}\n\nFORMAT:\nReturn strictly valid JSON that conforms to this JSON Schema.\n"
            f"Do not include any extra text, code fences, or commentary.\n"
            f"JSON_SCHEMA:\n{schema_str}\n"
        )
    return prompt
