def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}


def test_get_playlist_ok(client):
    res = client.get("/playlists/demo")
    assert res.status_code == 200
    data = res.json()
    assert data["playlistId"] == "demo"
    assert data["title"] in ("Demo", "Playlist demo")  # depending on repo impl
    assert len(data["tracks"]) == 2


def test_sort_playlist_by_title(client):
    # Sort
    res = client.post("/playlists/demo/sort", params={"rule_name": "by_title"})
    assert res.status_code == 200
    payload = res.json()
    assert payload["status"] == "ok"
    assert payload["rule"] == "by_title"
    assert payload["count"] == 2

    # Fetch and verify order is A then b
    res2 = client.get("/playlists/demo")
    assert res2.status_code == 200
    tracks = res2.json()["tracks"]
    titles = [t["title"] for t in tracks]
    assert titles == ["A Song", "b Song"]


def test_sort_playlist_unsupported_rule(client):
    res = client.post("/playlists/demo/sort", params={"rule_name": "not_a_rule"})
    assert res.status_code == 400
    assert "Unsupported rule" in res.json()["detail"]
