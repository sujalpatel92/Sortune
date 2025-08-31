from __future__ import annotations

import sys
from types import SimpleNamespace

from sortune_ai.config import LLMConfig
from sortune_ai.factory import get_llm
from sortune_ai.providers import LangChainLLM


def test_get_llm_returns_langchain_impl():
    cfg = LLMConfig(provider="langchain", backend="openai", model="gpt-4o-mini", temperature=0.5)
    llm = get_llm(cfg)
    assert isinstance(llm, LangChainLLM)


def test_langchain_llm_generate_uses_mocked_chat(monkeypatch):
    # Build a fake ChatOpenAI that records calls and returns an object with .content
    calls = {}

    class FakeMessage:
        def __init__(self, content: str):
            self.content = content

    class FakeChatOpenAI:
        def __init__(self, model: str, **kwargs):
            calls["init"] = {"model": model, "kwargs": kwargs}

        def invoke(self, prompt: str, **kwargs):
            calls["invoke"] = {"prompt": prompt, "kwargs": kwargs}
            return FakeMessage('{"names": []}')

    # Inject fake module
    fake_mod = SimpleNamespace(ChatOpenAI=FakeChatOpenAI)
    monkeypatch.setitem(sys.modules, "langchain_openai", fake_mod)

    llm = LangChainLLM(model="gpt-4o-mini", backend="openai", default_temperature=0.3)
    out = llm.generate("hello world", temperature=0.2, seed=7, model_kwargs={"foo": "bar"})

    assert out == '{"names": []}'
    assert calls["init"]["model"] == "gpt-4o-mini"
    # default_temperature passed at construction
    assert calls["init"]["kwargs"].get("temperature") == 0.3
    # Per-call temperature overrides to 0.2 if supported
    assert calls["invoke"]["kwargs"].get("temperature") == 0.2
    # Seed forwarded when provided
    assert calls["invoke"]["kwargs"].get("seed") == 7
    # Extra kwargs forwarded
    assert calls["invoke"]["kwargs"].get("foo") == "bar"
