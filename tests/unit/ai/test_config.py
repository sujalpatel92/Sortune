from __future__ import annotations

from sortune_ai.config import LLMConfig, load_llm_config


def test_load_llm_config_defaults(monkeypatch):
    # Clear relevant env vars
    for k in [
        "SORTUNE_LLM_PROVIDER",
        "SORTUNE_LLM_BACKEND",
        "SORTUNE_LLM_MODEL",
        "SORTUNE_LLM_TEMPERATURE",
        "SORTUNE_LLM_SEED",
    ]:
        monkeypatch.delenv(k, raising=False)

    cfg = load_llm_config()
    assert isinstance(cfg, LLMConfig)
    assert cfg.provider == "langchain"
    assert cfg.backend == "openai"
    assert cfg.model == "gpt-4o-mini"
    assert cfg.temperature == 0.6
    assert cfg.seed is None


def test_load_llm_config_env_override(monkeypatch):
    monkeypatch.setenv("SORTUNE_LLM_PROVIDER", "langchain")
    monkeypatch.setenv("SORTUNE_LLM_BACKEND", "openai")
    monkeypatch.setenv("SORTUNE_LLM_MODEL", "gpt-4o")
    monkeypatch.setenv("SORTUNE_LLM_TEMPERATURE", "0.1")
    monkeypatch.setenv("SORTUNE_LLM_SEED", "123")

    cfg = load_llm_config()
    assert cfg.provider == "langchain"
    assert cfg.backend == "openai"
    assert cfg.model == "gpt-4o"
    assert cfg.temperature == 0.1
    assert cfg.seed == 123
