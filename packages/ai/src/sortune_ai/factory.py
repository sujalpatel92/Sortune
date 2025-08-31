from __future__ import annotations

from .base import BaseLLM, LLMRuntimeError
from .config import LLMConfig, load_llm_config
from .providers.langchain_llm import LangChainLLM


def get_llm(cfg: LLMConfig | None = None) -> BaseLLM:
    """
    Return a BaseLLM implementation based on configuration.

    Currently supported providers:
      - 'langchain' (backend: 'openai' only for now)

    Future: 'ollama' (via langchain_community or native client).
    """
    cfg = cfg or load_llm_config()
    provider = cfg.provider

    if provider == "langchain":
        return LangChainLLM(
            model=cfg.model, backend=cfg.backend, default_temperature=cfg.temperature
        )

    raise LLMRuntimeError(f"Unsupported SORTUNE_LLM_PROVIDER='{provider}'. Expected 'langchain'.")
