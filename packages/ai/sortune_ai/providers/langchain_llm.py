from __future__ import annotations

from typing import Any

from ..base import BaseLLM, LLMRuntimeError


class LangChainLLM(BaseLLM):
    """
    LangChain-backed LLM implementation.

    Notes:
    - Currently supports the 'openai' backend via `langchain-openai`'s `ChatOpenAI`.
    - Dependencies are imported lazily and a helpful error is raised if missing.
    - The 'seed' argument is passed via model_kwargs when supported by the backend.
    """

    def __init__(
        self,
        *,
        model: str,
        backend: str = "openai",
        default_temperature: float | None = None,
    ) -> None:
        self._model_id = model
        self._backend = backend
        self._default_temperature = default_temperature
        self._chat = None  # lazy

    # ---------- Public API ----------
    def generate(
        self,
        prompt: str,
        *,
        temperature: float | None = None,
        seed: int | None = None,
        model_kwargs: dict[str, Any] | None = None,
    ) -> str:
        chat = self._chat_model()
        # Merge kwargs with seed when applicable
        mk = dict(model_kwargs or {})
        if seed is not None:
            # Newer OpenAI models support 'seed'
            mk.setdefault("seed", seed)
        # Encourage strict JSON output when using OpenAI
        if self._backend == "openai":
            mk.setdefault("response_format", {"type": "json_object"})
        # Temperature priority: call > default
        temp = self._default_temperature if temperature is None else temperature
        try:
            # Most Chat* models accept a string input directly.
            msg = chat.invoke(
                prompt,
                **({"temperature": temp} if temp is not None else {}),
                **mk,
            )
        except TypeError:
            # Some versions expect temperature via constructor only; retry without passing.
            msg = chat.invoke(prompt, **mk)
        # msg may be a BaseMessage or string depending on version
        content = getattr(msg, "content", None)
        print(content)
        return content if isinstance(content, str) else str(msg)

    # ---------- Internals ----------
    def _chat_model(self):
        if self._chat is not None:
            return self._chat

        if self._backend == "openai":
            try:
                from langchain_openai import ChatOpenAI  # type: ignore
            except Exception as e:  # pragma: no cover
                raise LLMRuntimeError(
                    "langchain-openai is not installed. Add 'langchain-openai' to packages/ai "
                    "dependencies or install extra '[langchain]' when developing."
                ) from e
            # Note: temperature may be overridden per-call; set base default here.
            kwargs: dict[str, Any] = {}
            if self._default_temperature is not None:
                kwargs["temperature"] = self._default_temperature
            self._chat = ChatOpenAI(model=self._model_id, **kwargs)
            return self._chat

        raise LLMRuntimeError(
            f"Unsupported LangChain backend '{self._backend}'. Supported: 'openai'"
        )
