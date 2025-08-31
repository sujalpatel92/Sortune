from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from sortune_api.main import app


@pytest.fixture()
def client():
    return TestClient(app)


def test_suggest_playlist_names_success(monkeypatch, client: TestClient):
    # Patch the route's generate function to avoid real LLM calls
    from sortune_ai.schemas import PlaylistName, PlaylistSuggestions
    from sortune_api.routes import ai as ai_routes

    def fake_generate(*, context: str, count: int = 5, seed: int | None = None):
        return PlaylistSuggestions(names=[PlaylistName(title="Foo", subtitle=None, rationale="ok")])

    monkeypatch.setattr(ai_routes, "generate_playlist_name_suggestions", fake_generate)

    res = client.post(
        "/ai/suggest-playlist-names",
        json={"context": "some ctx", "count": 2},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["names"][0]["title"] == "Foo"


def test_suggest_playlist_names_bad_llm(monkeypatch, client: TestClient):
    from sortune_api.routes import ai as ai_routes

    def bad_generate(*, context: str, count: int = 5, seed: int | None = None):
        raise ValueError("invalid json from provider")

    monkeypatch.setattr(ai_routes, "generate_playlist_name_suggestions", bad_generate)

    res = client.post(
        "/ai/suggest-playlist-names",
        json={"context": "x"},
    )
    assert res.status_code == 502
    assert "invalid json" in res.json()["detail"]
