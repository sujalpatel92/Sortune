from __future__ import annotations

import json

import pytest
from sortune_ai.config import LLMConfig
from sortune_ai.playlist_namer import generate_playlist_name_suggestions


class DummyLLM:
    def __init__(self, response: str):
        self.response = response
        self.last = None

    def generate(self, prompt: str, *, temperature=None, seed=None, model_kwargs=None):
        # Record last call for assertions
        self.last = {
            "prompt": prompt,
            "temperature": temperature,
            "seed": seed,
            "model_kwargs": dict(model_kwargs or {}),
        }
        return self.response


def test_generate_playlist_name_suggestions_success(monkeypatch):
    # Prepare dummy JSON response matching schema
    resp = json.dumps(
        {
            "names": [
                {"title": "Lofi Breeze", "subtitle": None, "rationale": "Calm summer vibe."},
                {"title": "Sunset Jazz", "subtitle": "Evening", "rationale": "Smooth horns."},
            ]
        }
    )
    dummy = DummyLLM(resp)

    # Force config and provider
    cfg = LLMConfig(
        provider="langchain", backend="openai", model="gpt-4o-mini", temperature=0.4, seed=99
    )
    monkeypatch.setattr("sortune_ai.playlist_namer.load_llm_config", lambda: cfg)
    monkeypatch.setattr("sortune_ai.playlist_namer.get_llm", lambda _cfg: dummy)

    out = generate_playlist_name_suggestions(context="evening jazz", count=2)
    assert len(out.names) == 2
    # Seed should come from config since not provided to function
    assert dummy.last["seed"] == 99
    # Prompt should include SEED_HINT
    assert "SEED_HINT: 99" in dummy.last["prompt"]


def test_generate_playlist_name_suggestions_invalid_json(monkeypatch):
    dummy = DummyLLM("not json")
    cfg = LLMConfig(provider="langchain", backend="openai", model="gpt-4o-mini", temperature=0.4)
    monkeypatch.setattr("sortune_ai.playlist_namer.load_llm_config", lambda: cfg)
    monkeypatch.setattr("sortune_ai.playlist_namer.get_llm", lambda _cfg: dummy)

    with pytest.raises(ValueError):
        generate_playlist_name_suggestions(context="ctx")
