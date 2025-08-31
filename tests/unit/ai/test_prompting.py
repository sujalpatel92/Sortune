from __future__ import annotations

from sortune_ai.prompting import render_name_gen_prompt


def test_render_prompt_includes_count_and_context():
    prompt = render_name_gen_prompt(count=3, context="lofi summer vibes")
    assert "Generate 3 playlist names" in prompt
    assert "lofi summer vibes" in prompt
    assert "SEED_HINT" not in prompt


def test_render_prompt_includes_seed_hint_when_provided():
    prompt = render_name_gen_prompt(count=2, context="evening jazz", seed=42)
    assert "SEED_HINT: 42" in prompt
