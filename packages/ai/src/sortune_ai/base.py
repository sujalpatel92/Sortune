from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


class LLMRuntimeError(RuntimeError):
    """Raised when an underlying LLM provider is misconfigured or fails."""


@runtime_checkable
class BaseLLM(Protocol):
    """
    Minimal provider-agnostic LLM interface used by Sortune.

    Implementations should perform a single-turn generation given a rendered prompt
    and return the model text output.
    """

    def generate(
        self,
        prompt: str,
        *,
        temperature: float | None = None,
        seed: int | None = None,
        model_kwargs: dict[str, Any] | None = None,
    ) -> str:  # pragma: no cover - interface only
        ...
