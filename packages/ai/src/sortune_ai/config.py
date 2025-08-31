from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class LLMConfig:
    """
    LLM configuration loaded from environment variables.

    Env vars (with defaults):
      - SORTUNE_LLM_PROVIDER: provider name (default: 'langchain')
      - SORTUNE_LLM_BACKEND: backend within provider (e.g., 'openai') (default: 'openai')
      - SORTUNE_LLM_MODEL: model id/name (default: 'gpt-4o-mini')
      - SORTUNE_LLM_TEMPERATURE: float (default: 0.6)
      - SORTUNE_LLM_SEED: int (optional)
    """

    provider: str = "langchain"
    backend: str = "openai"
    model: str = "gpt-4o-mini"
    temperature: float = 0.6
    seed: int | None = None


def _float(env: str, default: float) -> float:
    v = os.getenv(env)
    try:
        return float(v) if v is not None else default
    except Exception:
        return default


def _int(env: str) -> int | None:
    v = os.getenv(env)
    try:
        return int(v) if v is not None and v != "" else None
    except Exception:
        return None


def load_llm_config() -> LLMConfig:
    return LLMConfig(
        provider=os.getenv("SORTUNE_LLM_PROVIDER", "langchain").strip().lower(),
        backend=os.getenv("SORTUNE_LLM_BACKEND", "openai").strip().lower(),
        model=os.getenv("SORTUNE_LLM_MODEL", "gpt-4o-mini").strip(),
        temperature=_float("SORTUNE_LLM_TEMPERATURE", 0.6),
        seed=_int("SORTUNE_LLM_SEED"),
    )
